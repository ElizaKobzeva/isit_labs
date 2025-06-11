let ACCESS_TOKEN_MY = null

if ('VKIDSDK' in window) {
    const VKID = window.VKIDSDK;

    VKID.Config.init({
        app: 53351443, // id app
        redirectUrl: 'http://localhost',
        responseMode: VKID.ConfigResponseMode.Callback,
        source: VKID.ConfigSource.LOWCODE,
        scope: 'wall photos status friends groups', // Заполните нужными доступами по необходимости
    });

    const oneTap = new VKID.OneTap();

    oneTap.render({
        container: document.currentScript.parentElement,
        showAlternativeLogin: true
    })
        .on(VKID.WidgetEvents.ERROR, vkidOnError)
        .on(VKID.OneTapInternalEvents.LOGIN_SUCCESS, function (payload) {
            const code = payload.code;
            const deviceId = payload.device_id;

            VKID.Auth.exchangeCode(code, deviceId)
                .then(vkidOnSuccess)
                .catch(vkidOnError);
        });

    function vkidOnSuccess(data) {
        alert("вход выполнен!");
        console.log(data);
        //console.log(data.user_id);
        //console.log(data.access_token);
        ACCESS_TOKEN_MY = data.access_token;
        showField();
    }

    function vkidOnError(error) {
        //console.log('возникла непредвиденная ошшибка!');
    }
}


function showField() {
    //console.log(ACCESS_TOKEN_MY);
    document.getElementById("form").style.display = "block";
}

function set_like() {
    let owner_id = document.getElementById("owner_id").value;
    let post_id = document.getElementById("post_id").value;

    if (owner_id == "" || post_id == "") {
        alert("заполните все поля!");
        return;
    }

    let res = $.getJSON({

        // лайк на пост пользователя:

        url: `https://api.vk.com/method/likes.add?type=post&owner_id=${owner_id}&item_id=${post_id}&access_token=${ACCESS_TOKEN_MY}&v=5.199`,

        jsonp: "callback",
        dataType: "jsonp"
    }).done(function (data) {
        console.log(data);

        if (data.response == undefined) {
            alert("ошибка, вероятно введены неверные значения!");
        } else {
            alert("успех!");
        }
    });
}

function set_comment() {
    let owner_id = document.getElementById("owner_id").value;
    let post_id = document.getElementById("post_id").value;
    let comment = document.getElementById("comment").value;

    if (owner_id == "" || post_id == "" || comment == "") {
        alert("заполните все поля!");
        return;
    }

    let res = $.getJSON({
        //comment(for post in group - set - < -124151 >) where 124151 - id of group in VK
        // for user NO - before id !
        //for user:
        url: `https://api.vk.com/method/wall.createComment?owner_id=${owner_id}&post_id=${post_id}&message=${comment}&access_token=${ACCESS_TOKEN_MY}&v=5.199`,

        jsonp: "callback",
        dataType: "jsonp"
    }).done(function (data) {
        console.log(data);

        if (data.response == undefined) {
            alert("ошибка, вероятно введены неверные значения!");
        } else {
            alert("успех!");
        }
    });
}