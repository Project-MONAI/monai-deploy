var express = require('express');
var router = express.Router();
var { AMQPClient } = require('@cloudamqp/amqp-client');

async function run() {
  try {
    const amqp = new AMQPClient("amqp://localhost")
    const conn = await amqp.connect()
    const ch = await conn.channel()
    const q = await ch.queue()
    const consumer = await q.subscribe({noAck: true}, async (msg) => {
      console.log(msg.bodyToString())
      await consumer.cancel()
    })
    await q.publish("Hello World", {deliveryMode: 2})
    await consumer.wait() // will block until consumer is canceled or throw an error if server closed channel/connection
    await conn.close()
  } catch (e) {
    console.error("ERROR", e)
    e.connection.close()
    setTimeout(run, 1000) // will try to reconnect in 1s
  }
}


/* Send Rabbit Message. */
router.get('/', function(req, res, next) {
  run().then(() => {
    res.status(200).send("Passed");
  });
});

module.exports = router;
