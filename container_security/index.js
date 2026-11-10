const http = require("http");
const _ = require("lodash");
const server = http.createServer((req, res) => {
  const body = _.merge({ status: "ok" }, { service: "checkout" });
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify(body));
});
server.listen(3000, () => console.log("checkout-service di port 3000"));
