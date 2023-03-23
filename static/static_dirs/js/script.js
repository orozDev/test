const setAnswer = (element) => {
    const test_id = document.querySelector('#test_id').textContent
    const object = JSON.parse(element.value)

    axios.get(`/ajax/set_answer/${test_id}/`, {params: {...object}})
    .then(response => console.log('success'))
    .catch(error => {
        if (error.response.status === 400) alert(error.response.data.message)
        else if (error.response.status === 404) alert('Тест не найдено!')
        else alert('Ошибка сети!')
    })
}