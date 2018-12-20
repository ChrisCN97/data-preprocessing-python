
let data_loaded = false // 是否已经有数据被加载
let ft_input_path = $('#ft-input-path')
let main_input_path = $('#main-input-path')
let main_input_size = $('#main-input-size')
let data_preview = $('#data-preview')
let image_display = $('#big-image-display')
let thumbnail_container = $('#thumbnail-container')

const ResultType = {
    success: 0,
    failed: 1
}

const path_seperator = detectOS().startsWith('Win') ? '\\' : '/'

// 解析 python 传过来的 json 数据
const wrapcall = (consumer) => {
    return (data) => {
        data = JSON.parse(data)
        if (data.type == ResultType.success) {
            consumer(data.data, data.ext)
        }
        else {
            notify('danger', data.desc || 'unknown error occured')
        }
    }
}
// 通知
const notify = (type, msg, hasClose=false, duration=2000) => {
    let close = hasClose ? `<a href="#" class="close" data-dismiss="alert">&times;</a>` : '';
    let notify = $(`
        <div class="align-center alert alert-` + type + `">`
            + close + `
            <strong>` + msg + `</strong>
        </div>`)
    $('#main-container').append(notify)
    if (!hasClose) {
        setTimeout(() => notify.remove(), duration)
    }
}
// 输出数据到数据预览块
const preview_data = (col_keys, row_keys, at) => {
    let col_num = col_keys.length, row_num = row_keys.length
    // 清空预览
    data_preview.html('')
    // 生成 thead
    let thead = $('<thead></thead>')
    let thead_tr = $('<tr></tr>')
    thead_tr.append('<th></th>')
    for (let item of col_keys) {
        thead_tr.append(`<th>` + item + `</th>`)
    }
    thead.append(thead_tr)
    data_preview.append(thead)
    // 生成 tbody
    let tbody = $('<tbody></tbody>')
    for (let r = 0; r < row_num; r++) {
        let tbody_tr = $('<tr></tr>')
        tbody_tr.append(`<td>` + row_keys[r] + `</td>`)
        for (let c = 0; c < col_num; c++) {
            tbody_tr.append(`<td>` + at(c, r) + `</td>`)
        }
        tbody.append(tbody_tr)
    }
    data_preview.append(tbody)
}
// 输出数据规模，并调用 preview_data
const load_data = (json_data) => {
    data = JSON.parse(json_data)
    let col_keys, row_keys
    const at = (c, r) => data[col_keys[c]][row_keys[r]]
    attrs = col_keys = Object.keys(data)
    if (col_keys.length) {
        row_keys = Object.keys(data[col_keys[0]])
        main_input_size.text(row_keys.length + '行 * ' + col_keys.length + '列')
        preview_data(col_keys, row_keys, at)
    }
}
// 显示属性列，用于选择    
const display_attrs = () => {
    let c = $('#radio-container').html('')
    let row = $('<div class="row"></div>'), row_sz = 0, i = 0
    for (let attr of attrs) {
        row.append(`
        <div class="col-xs-3 col-sm-3">
            <label class="radio-inline">
                <input type="radio" name="radio"  value="` + i + `">` + attr + `
            </label>
        </div>`)
        row_sz++
        i++
        if (row_sz == 4) {
            row_sz = 0
            c.append(row)
            row = $('<div class="row"></div>')
        }
    }
    if (row_sz != 4) {
        c.append(row)
    }
    c.find('input').eq(0)[0].checked = true
}
const display_as_modal = () => {
    if (attrs) {
        display_attrs()
        as_modal.modal()
    }
    else notify('warning', '没有属性列，未加载数据')
}
// 添加图片到历史视图
const display_image = (b64_data, mid) => {
    let div = $(`<div class="col-sm-6 col-md-3"><a class="thumbnail"></a></div>`)
    let img = document.createElement('img')
    img.mid = mid
    img.src = 'data:image/png;base64,' + b64_data
    div.find('a').append(img)

    let c = $('#thumbnail-container')
    let rows = c.find('.row'), row = null, index = 0

    // 初始时为空，添加第一行
    if (rows.length == 0) {
        row = $('<div class="row"></div>')
        c.append(row)
    }
    else {
        index += (rows.length - 1) * 4
        row = rows.last()
    }

    let row_sz = row.children('div').length

    // 一行最多显示 4 张图片，该行已满，创建新行
    if (row_sz == 4) {
        row = $('<div class="row"></div>')
        c.append(row)
    }

    index += row_sz
    // 监听 click 事件
    $(img).click(() => image_display.show(index))
    row.append(div)
}

let attrs = null
let visual_callback = null
let ft_modal = $('#file-explorer')
let as_modal = $('#attr-selector')

/* 文件浏览器 */

let ft = new FileTree((path, resolve_view) =>
    eel.open_path(path)(wrapcall( (data) => resolve_view(data) )) // on click path
, (path) => ft_input_path.text(path)) // on click file

// 初始化文件浏览器，使用工作目录作为文件树根节点
eel.get_cwd()(wrapcall(
    (cwd) => $('#ft-container').append(ft.render({ name: cwd, type: 'dir'}))
))

// 后退按钮，读取父目录
$('#btn-ft-backup').click(() => ft.load_parent())

// 选择文件按钮，绑定 click 事件
$('#btn-ft-confirm').click(() => {
    let path = ft_input_path.text()
    if (path) {
        main_input_path.text(path)
        ft_modal.modal('toggle')
        eel.read_file(path)(wrapcall(
            (data) => {
                load_data(data)
                data_loaded = true
                notify('success', '数据加载成功')
            }
        ))
    }
    else alert('请选择一个数据文件')
})

/* 属性选择器 */
$('#btn-as-confirm').click(() => {
    if (visual_callback) {
        let radios = $('#radio-container').find('input')
        for (let i = 0, sz = radios.length; i < sz; i++) {
            if (radios.eq(i)[0].checked) {
                visual_callback(attrs[radios.eq(i).val()])
                break
            }
        }
    }
    else notify('danger', 'unknown error while processing btn-as-confirm#click')
    as_modal.modal('toggle')
})

/* 数据预览 */

let btn_refresh = $('#btn-refresh')
btn_refresh.tooltip()
btn_refresh.click(() => {
    let path = main_input_path.text()
    if (path) {
        if (!btn_refresh.refreshing) {
            btn_refresh.refreshing = true
            eel.read_file(path)(wrapcall(
                (data) => {
                    load_data(data)
                    btn_refresh.refreshing = false
                    notify('success', '刷新成功')
                }
            ))
        }
        else notify('warning', '请勿频繁刷新')
    }
    else notify('warning', '没有选择数据文件')
})

/* 轮播视图 */

image_display.set = (dist = 0) => {
    let imgs = thumbnail_container.find('img')
    let group = image_display.find('.item')

    let index = image_display.image_index
    let pos = image_display.image_position
    if (dist > 0) {
        index = (index == imgs.length - 1) ? 0 : index + 1
        pos = (pos == 2) ? 0 : pos + 1
    }
    else if (dist < 0) {
        index = (index == 0) ? imgs.length - 1 : index - 1
        pos = (pos == 0) ? 2 : pos - 1
    }
    else {
        let next_index = (index == imgs.length - 1) ? 0 : index + 1
        let next_pos = (pos == 2) ? 0 : pos + 1
        group.eq(next_pos).children('img').attr('src', imgs.eq(next_index).attr('src'))

        let prev_index = (index == 0) ? imgs.length - 1 : index - 1
        let prev_pos = (pos == 0) ? 2 : pos - 1
        group.eq(prev_pos).children('img').attr('src', imgs.eq(prev_index).attr('src'))
    }
    group.eq(pos).children('img').attr('src', imgs.eq(index).attr('src'))
    image_display.image_index = index
    image_display.image_position = pos
}

image_display.prev_set = () => image_display.set(-1)

image_display.next_set = () => image_display.set(1)

image_display.show = (index) => {
    image_display.image_index = index // 正在放映的图片的索引
    image_display.image_position = 0 // 图片在轮播组中的位置
    image_display.set()
    image_display.modal('toggle')
}

image_display.hide = () => {
    image_display.modal('toggle')
}

$("#btn-id-prev").click(() => image_display.prev_set())
$("#btn-id-next").click(() => image_display.next_set())
$('#btn-id-close').click(() => image_display.hide())

/* other */

$('#btn-save').click(() => {
    eel.save_data()(wrapcall(
        (output_path) => notify('success', 'output to: ' + output_path)
    ))
})

const call_eel = (name, method) => {
    if (data_loaded) {
        eel[name](method)(wrapcall(
            (data) => {
                load_data(data)
                notify('success', name + ' 成功')
            }
        ))
    }
    else notify('warning', '无数据')
}

// 空缺值处理

$('#null-process-mean').click(() => call_eel('null_process', 0))
$('#null-process-var').click(() => call_eel('null_process', 1))
$('#null-process-normal').click(() => call_eel('null_process', 2))

// 噪音处理

$('#noise-process-avg').click(() => call_eel('noise_process', 0))
$('#noise-process-border').click(() => call_eel('noise_process', 1))
$('#noise-process-mid').click(() => call_eel('noise_process', 2))

// 数据规范化

$('#normalize-min-max').click(() => call_eel('normalize', 0))
$('#normalize-z-score').click(() => call_eel('normalize', 1))
$('#normalize-calibrating').click(() => call_eel('normalize', 2))

// 数据可视化

$('#visual-bar').click(() => {
    display_as_modal()
    visual_callback = (label) => {
        eel.draw_bar(label)(wrapcall( (data, mid) => display_image(data, mid) ))
    }
})

$('#visual-line').click(() => {
    display_as_modal()
    visual_callback = (label) => {
        eel.draw_line(label)(wrapcall( (data, mid) => display_image(data, mid) ))
    }
})

$('#visual-pie').click(() => {
    display_as_modal()
    visual_callback = (label) => {
        eel.draw_pie(label)(wrapcall( (data, mid) => display_image(data, mid) ))
    }
})
