export function clearFields(fields) {
  for (let field of fields) {
    field.value = '';
  }
}

export function disableFields(fields) {
  for (let field of fields) {
    field.disabled = true;
  }
}

export function enableFields(fields) {
  for (let field of fields) {
    field.disabled = false;
  }
}
