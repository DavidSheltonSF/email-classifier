export function addClassToElements(elements, elementCLass) {
  for (let element of elements) {
    element.classList.add(elementCLass);
  }
}

export function removeClassFromElements(elements, elementCLass) {
  for (let element of elements) {
    element.classList.remove(elementCLass);
  }
}
