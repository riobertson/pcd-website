// ============================================================================
//  /api/send-sms.js  —  Purpose Church of Denton
//  Vercel Serverless Function that relays text messages to Twilio.
//
//  WHY THIS EXISTS:
//  Twilio's Auth Token is a SECRET. It must never appear in the dashboard's
//  HTML/JavaScript (anyone could "View Source" and steal it). This function
//  runs on Vercel's server, holds the token in an environment variable, and
//  the dashboard simply calls this endpoint. The token never reaches a browser.
//
//  SET THESE IN VERCEL  (Project → Settings → Environment Variables):
//    TWILIO_ACCOUNT_SID    your Account SID  (starts with AC...)
//    TWILIO_AUTH_TOKEN     your Auth Token   (KEEP SECRET)
//    TWILIO_FROM_NUMBER    your Twilio number in +1XXXXXXXXXX format
//    DASHBOARD_SMS_SECRET  (optional) a soft gate; if set, the dashboard must
//                          send the same value in the x-dashboard-secret header
// ============================================================================

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Optional soft gate (see note about limits in the README)
  const requiredSecret = process.env.DASHBOARD_SMS_SECRET;
  if (requiredSecret && req.headers['x-dashboard-secret'] !== requiredSecret) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const sid   = process.env.TWILIO_ACCOUNT_SID;
  const token = process.env.TWILIO_AUTH_TOKEN;
  const from  = process.env.TWILIO_FROM_NUMBER;
  if (!sid || !token || !from) {
    return res.status(500).json({ error: 'Twilio is not configured (missing environment variables).' });
  }

  let { to, message } = req.body || {};
  if (!message || !String(message).trim()) {
    return res.status(400).json({ error: 'Message text is required.' });
  }
  if (typeof to === 'string') to = [to];
  if (!Array.isArray(to) || to.length === 0) {
    return res.status(400).json({ error: 'At least one recipient is required.' });
  }
  // Safety cap per request — the dashboard sends in chunks of 25 anyway.
  if (to.length > 50) {
    return res.status(400).json({ error: 'Too many recipients in one request (max 50).' });
  }

  // Normalize a phone number to E.164 (assumes US if 10 digits)
  const toE164 = (raw) => {
    const s = String(raw).trim();
    if (s.startsWith('+')) return s;
    const d = s.replace(/\D/g, '');
    if (d.length === 10) return '+1' + d;
    if (d.length === 11 && d[0] === '1') return '+' + d;
    return null;
  };

  const url  = `https://api.twilio.com/2010-04-01/Accounts/${sid}/Messages.json`;
  const auth = 'Basic ' + Buffer.from(`${sid}:${token}`).toString('base64');

  const sendOne = async (recipient) => {
    const e164 = toE164(recipient);
    if (!e164) return { to: recipient, status: 'skipped', error: 'Invalid number' };
    try {
      const body = new URLSearchParams({ To: e164, From: from, Body: message });
      const r = await fetch(url, {
        method: 'POST',
        headers: { Authorization: auth, 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body.toString(),
      });
      const data = await r.json();
      return r.ok
        ? { to: e164, status: 'sent', sid: data.sid }
        : { to: e164, status: 'failed', error: data.message || 'Twilio error', code: data.code };
    } catch (e) {
      return { to: e164, status: 'failed', error: e.message };
    }
  };

  // Twilio's create-message call returns quickly ("queued"), so sending the
  // whole chunk in parallel is fast and stays well under Vercel's timeout.
  const results = await Promise.all(to.map(sendOne));
  const sent = results.filter((r) => r.status === 'sent').length;
  return res.status(200).json({ ok: true, sent, failed: results.length - sent, results });
}
