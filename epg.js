import https from 'https';

const req = https.get('https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?offset=0&channel_id=173&langId=6', function (res) {
  const chunks = [];

  res.on('data', function (chunk) {
    chunks.push(chunk);
  });

  res.on('end', function () {
    const body = Buffer.concat(chunks);
    console.log(body.toString());
  });
});
