import fs from 'fs';

async function test() {
  const formData = new FormData();
  formData.append('title', 'Backend Engineer');
  formData.append('content', 'Need a dev');

  console.log('Testing job creation via proxy...');
  let res = await fetch('http://localhost:3000/api/proxy/job-descriptions/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: 'Backend Engineer', content: 'Need a dev' })
  });
  console.log('Job status:', res.status, await res.text());

  console.log('Testing file upload via proxy...');
  const formDataFile = new FormData();
  const fileBlob = new Blob([fs.readFileSync('C:/Users/Administrator/Documents/résumé.pdf')], { type: 'application/pdf' });
  formDataFile.append('file', fileBlob, 'résumé.pdf');

  res = await fetch('http://localhost:3000/api/proxy/cvs/', {
    method: 'POST',
    body: formDataFile
  });
  console.log('File upload status:', res.status, await res.text());
}

test();
