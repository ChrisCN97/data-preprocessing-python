
class FileTree {
    constructor(onOpenDir, onOpenFile) {
        this.onOpenDir = onOpenDir
        this.onOpenFile = onOpenFile
        this.root_path = undefined
        this.root = undefined
    }

    get_path(elem) {
        let path = []
        let jq = $(elem)
        while (!jq.is('ft')) {
            path.push(jq.children('span').html())
            jq = jq.parent()
        }
        path.reverse()
        path = path.join(path_seperator)
        return path
    }

    resolve(root, data) {
        // 按类型排序并遍历子节点
        const resolve_array = (c) => {
            if (c) {
                let sz = c.length
                let i = 0, j = 0, tmp_item = undefined
                for (; i < sz && c[i].type == 'dir'; i++) { // 跳过开始部分连续的 dir
                    this.resolve(elem, c[i])
                }
                j = i
                for (; i < sz && j < sz; i++) {
                    if (c[i].type == 'file') {
                        for (; j < sz && c[j].type == 'file'; j++); // 往后查找 dir 类型的 item
                        if (j < sz) { // 交换，使所有 dir 都在 file 前面
                            tmp_item = c[j]
                            c[j] = c[i]
                            c[i] = tmp_item
                            j++
                        }
                    }
                    this.resolve(elem, c[i])
                }
                for (; i < sz; i++) { // 解析剩下的所有 file
                    this.resolve(elem, c[i])
                }
            }
        }
        let elem
        if (data.type == 'dir') {
            elem = document.createElement('ft-dir')
            // 背景
            $(elem).append('<a class="ft-back"></a>');
            // 名称
            $(elem).append('<span>' + data.name + '</span>')
            // 折叠、展开
            elem.folded = true
            elem.loaded = false
            elem.load = () => {
                if (this.onOpenDir) {
                    this.onOpenDir(this.get_path(elem), (sub_data) => resolve_array(sub_data))
                    elem.loaded = true
                    elem.folded = false
                }
            }
            elem.fold = () => {
                if (!elem.folded) {
                    $(elem).children().css('display', 'none')
                    $(elem).children('span').css('display', 'block')
                    elem.folded = true
                    return true
                }
                return false
            }
            elem.expand = () => {
                if (elem.folded) {
                    $(elem).children().css('display', 'block')
                    elem.folded = false
                    return true
                }
                return false
            }
            $(elem).click((evt) => {
                if (!elem.loaded)
                    elem.load()
                else {
                    if (!elem.fold())
                        elem.expand()
                }
                evt.stopPropagation()
                return false
            })
            resolve_array(data.children)
        }
        else {
            elem = document.createElement('ft-file')
            $(elem).append('<a class="ft-back"></a>');
            $(elem).append('<span>' + data.name + '</span>')
            $(elem).click((evt) => {
                if (this.onOpenFile) {
                    this.onOpenFile(this.get_path(elem))
                }
                evt.stopPropagation()
                return false
            })
        }
        $(root).append(elem)
    }

    load_parent() {
        $(this.root).children().first().remove()
        this.root_path.pop()
        if (this.root_path) {
            this.resolve(this.root, {name: this.root_path.join(path_seperator), type: 'dir'})
            $(this.root).children().first().click()
        }
    }

    render(data) {
        this.root_path = data.name.split(path_seperator)
        this.root = document.createElement('ft')
        this.resolve(this.root, data)
        return this.root
    }

}