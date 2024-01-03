login to the server
```bash
ssh -i foodcom.pem ubuntu@3.34.76.235
```

Installing node js
```bash
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Detect if the port is running
```bash
sudo fuser 8000/tcp
```

Kill that port
```bash
sudo kill -9 111 111 111
```

Start a service
```bash
sudo systemctl start <service name>
```

Stop a service 
```bash
sudo systemctl stop <service name>
```

Restart a service 
```bash
sudo systemctl restart <service name>
```

Reload services - necessary everytime code is changed
```bash
sudo systemctl daemon-reload
```

Services:
- foodcom-backend
- foodcom-frontend
- foodcom-bot
- caddy

Npm build
```bash
sudo npm run build
```
if it fails - > stop all services and restart the ubuntu machine, then stop services again, rerun the npm build, don't forget to run daemon-reload


Backend deployment
```bash
gunicorn -b 0.0.0.0:8000 appBack.wsgi:application
```

CaddyFile
```
food-c.co.kr {
        reverse_proxy localhost:3000
}

api.food-c.co.kr {
        reverse_proxy localhost:8000
}

xn--hy1bw80c81d.com {
        reverse_proxy localhost:3000
}

api.xn--hy1bw80c81d.com {
        reverse_proxy localhost:8000
}
```

Early deployment (FAILED)
```js
  "scripts": {
    "dev": "node server.js",
    "build": "next build",
    "start": "NODE_ENV=production node server.js",
    "lint": "next lint",
    "test": "jest --watch"
  },
```

server.js 
```js
const { createServer } = require('https');
const { parse } = require('url');
const next = require('next');
const fs = require('fs');

const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

const httpsOptions = {
  key: fs.readFileSync('/etc/letsencrypt/live/food-c.co.kr/privkey.pem'),
  cert: fs.readFileSync('/etc/letsencrypt/live/food-c.co.kr/cert.pem'),
  ca: fs.readFileSync('/etc/letsencrypt/live/food-c.co.kr/chain.pem'),
};

app.prepare().then(() => {
  createServer(httpsOptions, (req, res) => {
    const parsedUrl = parse(req.url, true);
    handle(req, res, parsedUrl);
  }).listen(443, (err) => {
    if (err) throw err;
    console.log('> Ready on https://food-c.co.kr');
  });
});
```
