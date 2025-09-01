import {
  addClassToElements,
  removeClassFromElements,
} from './helpers/elementClass.js';
import { clearFields, disableFields, enableFields } from './helpers/form.js';

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

const hostMap = {
  localhost: 'http://localhost',
  render: 'https://desafio-autou-back.onrender.com',
};

classifyButton.addEventListener('click', async (e) => {
  try {
    e.preventDefault();
    emailSubjectInput.disabled = false;
    emailSubjectInput.classList.remove('uploaded-pdf');
    emailBodyInput.disabled = false;
    emailBodyInput.classList.remove('uploaded-pdf');
    emailSubjectOutput.value = '';
    emailBodyOutput.value = '';
    messageEmailType.value = '';
    messageEmailType.classList.remove('positive-message-text-color');
    messageEmailType.classList.remove('negative-message-text-color');
    copyStatusMessage.textContent = '';
    copyStatusMessage.classList.remove('positive-message-text-color');
    copyStatusMessage.classList.remove('negative-message-text-color');

    let response = null;

    if (fileInput.files.length > 0) {
      const formData = new FormData();
      formData.append('file', fileInput.files[0]);

      response = await fetch(
        `${hostMap['render']}:8000/classify/email-pdf`,
        {
          method: 'POST',
          body: formData,
        }
      );
    } else {
      response = await fetch(
        `${hostMap['render']}:8000/classify/email`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            subject: emailSubjectInput.value,
            body: emailBodyInput.value,
          }),
        }
      );
    }

    const responseJson = await response.json();
    const data = responseJson.data;
    const result = data.result;
    const reply = data.reply;
    console.log(data);

    emailSubjectOutput.value = reply.subject;
    emailBodyOutput.value = reply.body;

    messageEmailType.textContent = result.label;
    console.log(result.label);

    const messageColor =
      result.label === 'produtivo' ? 'positive-message' : 'negative-message';
    messageEmailType.classList.add(messageColor);
  } catch (error) {
    console.log(error);
  }
});

uploadPdfButton.addEventListener('click', (e) => {
  e.preventDefault();
  console.log(fileInput.value);
  fileInput.click();
});

fileInput.addEventListener('change', () => {
  const fields = [emailSubjectInput, emailBodyInput];
  const file = fileInput.files[0];
  emailBodyInput.value = file.name;
  addClassToElements([emailBodyInput], 'uploaded-pdf');
  disableFields(fields);
});

clearFieldsButton.addEventListener('click', (e) => {
  e.preventDefault();
  fileInput.value = '';
  const fields = [emailSubjectInput, emailBodyInput];
  clearFields(fields);
  enableFields(fields);
  removeClassFromElements(fields, 'uploaded-pdf');
});

copyButton.addEventListener('click', async (e) => {
  e.preventDefault();
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
      emailBodyInput.value = joinedBody;
    };
    reader.readAsText(file);
  }
});
