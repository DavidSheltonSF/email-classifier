const emailSubjectInput = document.querySelector('.input-email-subject');
const emailBodyInput = document.querySelector('.input-email-body');
const classifyButton = document.querySelector('.btn-classify');

const emailSubjectOutput = document.querySelector('.output-email-subject');
const emailBodyOutput = document.querySelector('.output-email-body');
const messageEmailType = document.querySelector('.msg-email-type');
const copyButton = document.querySelector('.btn-copy');
const copyStatusMessage = document.querySelector('.msg-copy-status');

classifyButton.addEventListener('click', async () => {
  try {
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

    emailSubjectInput.value = '';
    emailBodyInput.value = '';

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
