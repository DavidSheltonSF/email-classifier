const emailSubjectInput = document.querySelector('.input-email-subject');
const emailBodyInput = document.querySelector('.input-email-body');
const classifyButton = document.querySelector('.btn-classify');
const fileInput = document.querySelector('.file-input');
const uploadPdfButton = document.querySelector('.btn-upload-pdf');
const clearFieldsButton = document.querySelector('.btn-clear-fields');

const emailSubjectOutput = document.querySelector('.output-email-subject');
const emailBodyOutput = document.querySelector('.output-email-body');
const messageEmailType = document.querySelector('.msg-email-type');
const copyButton = document.querySelector('.btn-copy');
const copyStatusMessage = document.querySelector('.msg-copy-status');

classifyButton.addEventListener('click', async () => {
  try {
    emailSubjectInput.disabled = false;
    emailSubjectInput.classList.remove('uploaded-pdf');
    emailBodyInput.disabled = false;
    emailBodyInput.classList.remove('uploaded-pdf');
    emailSubjectOutput.value = '';
    emailBodyOutput.value = '';
    messageEmailType.textContent = '';
    messageEmailType.classList.remove('positive-message-text-color');
    messageEmailType.classList.remove('negative-message-text-color');
    copyStatusMessage.textContent = '';
    copyStatusMessage.classList.remove('positive-message-text-color');
    copyStatusMessage.classList.remove('negative-message-text-color');

    const response = await fetch('http://localhost:8000/classify/email', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        subject: emailSubjectInput.value,
        body: emailBodyInput.value,
      }),
    });

    const responseJson = await response.json();
    const data = responseJson.data;
    const result = data.result;
    const reply = data.reply;
    console.log(data);

    emailSubjectOutput.value = reply.subject;
    emailBodyOutput.value = reply.body;

    messageEmailType.textContent = result.label;

    const messageColor =
      result.label === 'produtivo' ? 'positive-message' : 'negative-message';
    messageEmailType.classList.add(messageColor);
  } catch (error) {
    console.log(error);
  }
});

uploadPdfButton.addEventListener('click', () => {
  fileInput.click()
})

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  emailBodyInput.textContent = file.name
  emailBodyInput.classList.add('uploaded-pdf');
  emailSubjectInput.disabled = true;
  emailBodyInput.disabled = true;
})

clearFieldsButton.addEventListener('click', () => {
   emailSubjectInput.value = '';
   emailBodyInput.value = '';
   emailSubjectInput.disabled = false;
   emailSubjectInput.classList.remove('uploaded-pdf');
   emailBodyInput.disabled = false;
   emailBodyInput.classList.remove('uploaded-pdf');
})

copyButton.addEventListener('click', async () => {
  const text = `${emailSubjectOutput.value}\n\n${emailBodyOutput.value}`;

  let message = '';
  let messageColor = '';

  navigator.clipboard
    .writeText(text)
    .then(() => {
      console.log('Texto copiado com sucesso!');
      message = 'Email copiado!';
      messageColor = 'positive-message-text-color';
    })
    .catch((err) => {
      console.log(err);
      message = 'Algo deu errado!';
      messageColor = 'negative-message-text-color';
    })
    .finally(() => {
      {
        copyStatusMessage.textContent = message;
        copyStatusMessage.classList.add(messageColor);
      }
    });
});

const dropZone = document.querySelector('.dropzone');
const dragOverIcon = document.querySelector('.dragover-icon');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach((eventName) => {
  dropZone.addEventListener(eventName, (e) => e.preventDefault());
});

dropZone.addEventListener('dragover', (e) => {
  dragOverIcon.classList.remove('display-none');
});

dropZone.addEventListener('dragleave', (e) => {
  if (!dropZone.contains(e.relatedTarget)) {
    dragOverIcon.classList.add('display-none');
  }
});

dropZone.addEventListener('drop', async (e) => {
  dragOverIcon.classList.add('display-none');

  const file = e.dataTransfer.files[0];

  if (!file) {
    return;
  }
  if (file.type == 'text/plain') {
    const reader = new FileReader();
    reader.onload = () => {
      const splitedEmail = reader.result.split('\n');
      const subject = splitedEmail.shift();
      const joinedBody = splitedEmail.join('\n');
      emailSubjectInput.value = subject;
      emailBodyInput.textContent = joinedBody;
    };
    reader.readAsText(file);
  }
});
