
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
            notify('danger', data.desc || 'unknown error occured', hasClose = true, align_center=false)
        }
    }
}

// 通知
const notify = (type, msg, hasClose=false, align_center=true) => {
    let notify = $(`
        <div class="alert alert-` + type + `">
            <p style="display: block; width: 100%; white-space: pre; word-break: break-all;">` + msg + `</p>
        </div>`)
    if (align_center) {
        notify.addClass('align-center')
    }
    if (hasClose) {
        notify.prepend(`<a href="#" class="close" data-dismiss="alert">&times;</a>`)
    }
    else {
        setTimeout(() => notify.remove(), 2000)
    } 
    $('#notify-box').append(notify)
}

let ft_modal = $('#file-explorer')

/* 计算控制 */

/* mpc 功能不可用 */
// let btn_enable_mpc = $('#btn-enable-mpc')
// btn_enable_mpc.click(() => {
//     if (btn_enable_mpc.active) {
//         eel.disable_mpc()(wrapcall(
//             () => {
//                 btn_enable_mpc.active = !btn_enable_mpc.active
//                 btn_enable_mpc.addClass('active')
//                 notify('succss', '已禁用多核运算')
//             }
//         ))
//     }
//     else {
//         eel.enable_mpc()(wrapcall(
//             () => {
//                 btn_enable_mpc.active = !btn_enable_mpc.active
//                 btn_enable_mpc.removeClass('active')
//                 notify('success', '已启用多核运算')
//             }
//         ))
//     }
// })

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

// 选择文件按钮，绑定 click 事件，负责加载数据以及重置视图
$('#btn-ft-confirm').click(() => {
    let path = ft_input_path.text()
    if (path) {
        if (path != main_input_path.text()) {
            main_input_path.text(path)
            eel.read_file(path)(wrapcall(
                (data) => {
                    data_loaded = true
                    ft_modal.modal('toggle')
                    load_data(data)
                    notify('success', '数据加载成功')
                }
            ))
        }
        else notify('warning', '数据已加载')
    }
    else notify('warning', '请选择一个数据文件')
})

/* 属性筛选器 */

let attrs = null

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

const get_checked_attr = () => {
    let radios = $('#radio-container').find('input')
    for (let i = 0, sz = radios.length; i < sz; i++) {
        if (radios.eq(i)[0].checked) {
            return attrs[radios.eq(i).val()]
        }
    }
}

let enable_attr_filter = true // 是否启用属性筛选，如果false，调用可视化接口会显示error
let btn_as_disable = $('#btn-as-disable')
btn_as_disable.click(() => {
    if (enable_attr_filter) {
        btn_as_disable.addClass('active')
        btn_as_disable.text('启用筛选')
        $('#radio-container').css('display', 'none')
    }
    else {
        btn_as_disable.removeClass('active')
        btn_as_disable.text('禁用筛选')
        $('#radio-container').css('display', 'block')
    }
    enable_attr_filter = !enable_attr_filter
})

/* 数据预览 */

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
    base = JSON.parse(json_data)
    if (base.data) {
        data = JSON.parse(base.data)
        let col_keys, row_keys
        const at = (c, r) => data[col_keys[c]][row_keys[r]]
        
        // 清空缩略视图
        $('#thumbnail-container').html('')

        // 设置属性筛选器
        attrs = col_keys = Object.keys(data)
        display_attrs()

        if (col_keys.length) {
            row_keys = Object.keys(data[col_keys[0]])
            main_input_size.text(base.nr + '行 * ' + base.nc + '列')
            preview_data(col_keys, row_keys, at)
        }
    }
}

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

/* 缩略视图 */

// 添加图片到缩略视图
const display_image = (b64_data, mid) => {
    let div = $(`<div class="col-sm-6 col-md-3 align-center"><div class="thumbnail"></div></div>`)
    let img = document.createElement('img')
    img.mid = mid
    img.src = 'data:image/png;base64,' + b64_data
    div.find('div').append(img).append(`<span>` + mid + `</span>`)

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

/* other */

$('#btn-save').click(() => {
    eel.save_data()(wrapcall(
        (output_dir) => notify('success', 'output to: ' + output_dir, hasClose=true)
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
    else notify('danger', '无数据')
}

const call_eel_visual = (name) => {
    if (data_loaded) {
        if (enable_attr_filter) {
            let label = get_checked_attr()
            eel[name](label)(wrapcall( (data, mid) => display_image(data, mid) ))
        }
        else notify('danger', '请启用属性筛选')
    }
    else notify('danger', '无数据')
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

$('#visual-bar').click( () => call_eel_visual('draw_bar') )
$('#visual-line').click( () => call_eel_visual('draw_line') )
$('#visual-pie').click( () => call_eel_visual('draw_pie') )
