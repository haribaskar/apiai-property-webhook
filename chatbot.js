(function () {
    var div = document.createElement("div");
    document.getElementsByTagName('body')[0].appendChild(div);
    div.outerHTML = "<div id='botDiv' style='height: 30px; position: fixed; bottom: 0; z-index: 1000; background-color: #fff'>   <div id='botTitleBar' style='height: 38px; width: 400px; position:relative; cursor: pointer;'></div><iframe width='400px' height='600px' src='https://webchat.botframework.com/embed/chefai?s=63ooGtafagg.cwA.4kA.T-oGtBB22ldUksxX462CnMJFd_DGRuZ1whAtrd578P8'></iframe></div>"; 

    document.querySelector('body').addEventListener('click', function (e) {
        e.target.matches = e.target.matches || e.target.msMatchesSelector;
        if (e.target.matches('#botTitleBar')) { 
            var botDiv = document.querySelector('#botDiv'); 
            botDiv.style.height = botDiv.style.height == '600px' ? '38px' : '600px';
        };
    });
    }());