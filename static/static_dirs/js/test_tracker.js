const test_id = document.getElementById('test_id').textContent
let left_time = Number(document.getElementById('left_time').textContent)
const left_time_container = document.getElementById('left_time_container')

setInterval(() => {
    left_time_container.innerHTML = convert_time(left_time)
    left_time--
    if(left_time < 1) window.location.href = `/complete_test/${test_id}/`
}, 1000)

const convert_time = seconds => {
    let minutes = Math.round(seconds / 60)
    let left_seconds = seconds % 60

    return `${minutes}:${left_seconds}`
}
