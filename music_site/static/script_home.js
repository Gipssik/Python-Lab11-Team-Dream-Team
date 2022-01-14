const renderContent = () => {
    const contentElemsArr = [...document.querySelectorAll(".info__context")];
    const textArr = contentElemsArr.map(item => item.innerText);
    const shortTextArr = textArr.map(elem =>
        elem.length > 40
            ? elem.substr(0, 37) + "..."
            : elem);

    contentElemsArr.forEach((elem, index) => {
        contentElemsArr[index].innerText = shortTextArr[index];
    })
}

document.addEventListener("DOMContentLoaded", renderContent);