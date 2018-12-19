
// 空缺值处理

$('#null-process-mean').click(() => {
    eel.null_process(0)
})

$('#null-process-var').click(() => {
    eel.null_process(1)
})

$('#null-process-normal').click(() => {
    eel.null_process(2)
})

// 噪音处理

$('#noise-process-avg').click(() => {
    eel.noise_process(0)
})

$('#noise-process-border').click(() => {
    eel.noise_process(1)
})

$('#noise-process-mid').click(() => {
    eel.noise_process(2)
})

// 数据规范化

$('#normalize-min-max').click(() => {
    eel.normalize(0)
})

$('#normalize-z-score').click(() => {
    eel.normalize(1)
})

$('#normalize-calibrating').click(() => {
    eel.normalize(2)
})

// 数据可视化

$('#visual-bar').click(() => {
    eel.draw_bar()
})

$('#visual-line').click(() => {
    eel.draw_line()
})

$('#visual-pie').click(() => {
    eel.draw_pie()
})

// data = eel.get_data()
// $('#data-preview').value(data)