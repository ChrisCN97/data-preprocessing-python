
let data = {
    'name': 'home',
    'type': 'dir',
    'children': [
        {
            'name': 'luncert',
            'type': 'dir',
            'children': [
                {
                    'name': '.profile',
                    'type': 'file'
                }
            ]
        },
        {
            'name': '.config',
            'type': 'file'
        }
    ]
}

let ftRender_resolve = (root, data) => {
    let tmp
    if (data.type == 'dir') {
        tmp = document.createElement('ft-dir')
        $(tmp).append('<a class="ft-back"></a>');
        $(tmp).append('<span>' + data.name + '</span>')
        // $(tmp).click()
        for (let item of data.children) {
            ftRender_resolve(tmp, item)
        }
    }
    else {
        tmp = document.createElement('ft-file')
        $(tmp).append('<a class="ft-back"></a>');
        $(tmp).append('<span>' + data.name + '</span>')
        // $(tmp).click()
    }
    $(root).append(tmp)
}

function ftRender(data) {
    let ft = document.createElement('ft')
    ftRender_resolve(ft, data)
    return ft
}