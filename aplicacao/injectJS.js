
    var buttons = document.getElementsByTagName('button');
    var button_style = 
    `
    background-color: #2ea44f; 
    border: 1px solid rgba(27, 31, 35, .15); 
    border-radius: 6px;
    box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
    box-sizing: border-box;
    color: #fff;
    cursor: pointer;
    display: inline-block;
    font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
    padding: 6px 16px;
    position: relative;
    text-align: center;
    text-decoration: none;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    vertical-align: middle;
    white-space: nowrap;
    `
    var label_style = 
    `
        background-color: rgb(0, 105, 146);
        color: white;
        border: 1px solid rgba(27, 31, 35, 0.15);
        border-radius: 6px;
        line-height: 20px;
        height: 22px;
        padding: 6px 16px;
        text-align: center;
        display: inline-block;
        margin-right: -20px;
    `
    var input_style = 
    `
        color: black;
        background: white;
        border-radius: 6px;
        font-size: 14px;
        line-height: 20px;
        padding: 6px 16px;
        text-align: center;
        width: 100;
    `
    var graph_style = `margin: 30px; box-shadow: 2px 2px 15px black;`

    for (let i = 0; i < buttons.length; i++) {
        let button = buttons[i];
        button.style.cssText = button_style
    }

    for(let i = 1; i <= 10; i++){
        var object = document.getElementById(i);
        if(i % 2 == 0){
            object.style.cssText = input_style
        }else{
            object.style.cssText = label_style
        }
    }

    var graph_ids = ['graph0', 'graph1', 'graph2']
    for(let i = 0; i < graph_ids.length; i++){
        var object = document.getElementById(graph_ids[i]);
        object.style.cssText += graph_style;
    }

    var sliders_labels_ids = ['15', '17']
    for(let i = 0; i < sliders_labels_ids.length; i++){
        var object = document.getElementById(sliders_labels_ids[i]);
        object.style.cssText += label_style;
        object.style.cssText += 'width: 1000;';
    }

    var body = document.body
    body_style = document.createElement('style');
    body_style.type = 'text/css';
    body.appendChild(body_style);
    body.style.cssText = 'text-align: -webkit-center;'
