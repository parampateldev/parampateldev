#!/usr/bin/env node
const { exec, spawn } = require('child_process');
const path = require('path');

// Change to parent directory so both website/ and projects/ are accessible
process.chdir('/Users/parampatel/parampatel-dev');

// Kill any existing server on port 8000
exec('lsof -ti:8000 | xargs kill -9 2>/dev/null', () => {
  console.log('Starting live-reload server...');
  console.log('Server will auto-reload when you make changes to files!');
  
  // Start live-server with auto-reload
  const liveServer = spawn('npx', ['--yes', 'live-server', '--port=8000', '--open=/website/', '--watch=website'], {
    stdio: 'inherit',
    shell: true
  });
  
  // Open browser after a delay
  setTimeout(() => {
    const platform = process.platform;
    let command;
    if (platform === 'darwin') {
      command = `open "http://localhost:8000/website/"`;
    } else if (platform === 'win32') {
      command = `start "http://localhost:8000/website/"`;
    } else {
      command = `xdg-open "http://localhost:8000/website/"`;
    }
    exec(command);
  }, 3000);
  
  console.log('\n✅ Live-reload server is running!');
  console.log('📝 Edit your files and they will auto-reload in the browser');
  console.log('🛑 Press Ctrl+C to stop the server\n');
  
  // Handle cleanup
  process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down server...');
    liveServer.kill();
    process.exit(0);
  });
  
  liveServer.on('exit', (code) => {
    process.exit(code);
  });
});
    let urlPath = req.url.split('?')[0]; // Remove query params
    
    // Default to website/index.html for root
    if (urlPath === '/' || urlPath === '/index.html') {
      urlPath = '/website/index.html';
    }
    
    // Resolve to absolute path
    let filePath = path.join(process.cwd(), urlPath);
    filePath = path.normalize(filePath);
    
    // Security check: ensure path is within the project directory
    const projectRoot = process.cwd();
    if (!filePath.startsWith(projectRoot)) {
      res.writeHead(403);
      res.end('Forbidden');
      return;
    }
    
    const extname = String(path.extname(filePath)).toLowerCase();
    const mimeTypes = {
      '.html': 'text/html',
      '.js': 'text/javascript',
      '.css': 'text/css',
      '.json': 'application/json',
      '.png': 'image/png',
      '.jpg': 'image/jpg',
      '.gif': 'image/gif',
      '.svg': 'image/svg+xml',
      '.ico': 'image/x-icon'
    };
    
    const contentType = mimeTypes[extname] || 'application/octet-stream';
    
    fs.readFile(filePath, (error, content) => {
      if (error) {
        if (error.code === 'ENOENT') {
          res.writeHead(404);
          res.end('File not found');
        } else {
          res.writeHead(500);
          res.end('Server error: ' + error.code);
        }
      } else {
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(content, 'utf-8');
      }
    });
  });
  
  server.listen(8000, () => {
    console.log('Server running at http://localhost:8000/');
    console.log('Opening browser...');
    
    // Open browser (default to website)
    const url = 'http://localhost:8000/website/';
    const platform = process.platform;
    
    let command;
    if (platform === 'darwin') {
      command = `open "${url}"`;
    } else if (platform === 'win32') {
      command = `start "${url}"`;
    } else {
      command = `xdg-open "${url}"`;
    }
    
    exec(command, (error) => {
      if (error) {
        console.log('Could not open browser automatically. Please open:', url);
      } else {
        console.log('Browser opened!');
      }
    });
  });
});

