console.log('Loading function');

const https = require('https');
const url = require('url');
// to get the slack hook url, go into slack admin and create a new "Incoming Webhook" integration
const slack_url = process.env.SLACK_URL;
console.log('slack_url: ' + slack_url);
const slack_req_opts = url.parse(slack_url);
slack_req_opts.method = 'POST';
slack_req_opts.headers = {'Content-Type': 'application/json'};

exports.handler = function(event, context) {
  (event.Records || []).forEach(function (rec) {
    if (rec.Sns) {
      var req = https.request(slack_req_opts, function (res) {
        if (res.statusCode === 200) {
          context.succeed('posted to slack');
        } else {
          context.fail('status code: ' + res.statusCode);
        }
      });

      req.on('error', function(e) {
        console.log('problem with request: ' + e.message);
        context.fail(e.message);
      });

      req.write(JSON.stringify({text: JSON.stringify(rec.Sns.Message, null, '  ')})); // for testing: , channel: '@vadim'

      req.end();
    }
  });
};
