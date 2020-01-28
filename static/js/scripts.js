let get_projects = ()=>{
    let project = []
    $( "#projectmenu li" ).each( function( index, element ){
        let info = $(this).data('info');
        let arr = info.split('-');
        project.push({
            'id': arr[0],
            'name' : arr[1]
        })
   });
   return project;
}

let get_outlines = ()=>{
    let outline = []
    $( "#outlinemenu li" ).each( function( index, element ){
        let info = $(this).data('info');
        let arr = info.split('-');
        outline.push({
            'id': arr[0],
            'name' : arr[1]
        })
    });
    return outline;
}

let project = get_projects()
let outline = get_outlines()


let showtask_adder = (type)=>{

    if(type){
        $('.imagevisuals').toggle()
        $('#newtask').toggle()
    }
    else{
        $('#addtask').toggle()
    }
    
}

$('#taskinput').on('input', function() {
     $('#inputsuggest').hide();
     let input = $('#taskinput').val()
     let blocks = input.split(' ');
     let currentblock = blocks[blocks.length - 1]
     let response = '';
     if((currentblock.length > 3) && ((currentblock.startsWith('/')) || (currentblock.startsWith('#'))))
     {
         suggestion_arr = (currentblock.startsWith('/')) ? suggestion_array(project,currentblock) : suggestion_array(outline,currentblock);
         if(suggestion_arr){
              suggestion_arr.map( (s) => {
                  response = response + `<a class="list-item" onclick="put_suggestion('${s.id}','${s.name}')">${s.name}</a>`;
              })
              $('#inputsuggest').html(response).show();
         }
     }
});

let suggestion_array = (dataset,currentblock)=>{
    let filtered_arr = [];
    search = currentblock.substr(1)
    dataset.filter( (p)=>{
         let term = p.name.substr(0,search.length).toUpperCase();
         if(search.toUpperCase() == term) {
             filtered_arr.push(p)
         }
    })
    return filtered_arr;
}

let put_suggestion = (input,name)=>{
    $('#inputsuggest').hide();
    let userinput = $('#taskinput').val()
    let blocks = userinput.split(' ');
    blocks.pop();
    blocks.push(`#${name}`);
    let finalinput = blocks.join(' ')
    $('#inputsuggest').data('outline',input);
    $('#taskinput').val(finalinput)
}

let task_input = (block)=>{
    let userinput = $('#taskinput').val()
    let outline   = $('#inputsuggest').data('outline');
    if(userinput.length > 3){

        $('#inputsuggest').data('outline','');
        $('#taskinput').val('')
        $(`#${block}task`).hide()

        let formatted_ip = format_imput(userinput);
        formatted_ip.outline = outline;       
        formatted_ip.csrfmiddlewaretoken =  $('input[name=csrfmiddlewaretoken]').val();

		 $.post("/new-task/",formatted_ip, function (response) {
             if(response.status == 'ok'){
                 let data = response.data[0];
                  location.reload();
                 //console.log(data)
             }
        });

    }
    
}

let finishtask = (id,status)=>{
     url = (status == 'True') ? 'restore' : 'finish';
     $.post(`/${url}-task/`,{'id' : id , 'status' : status }, function (data) {
        if(data.status == 'ok'){
            $(`#taskrow${id}`).fadeOut(1000);
        }
    });
}

let removetask = (id)=>{     
    $.post("/delete-task/",{'id' : id }, function (data) {
         if(data.status == 'ok'){
              $(`#taskrow${id}`).fadeOut(1000);
         }
    });
}


let format_imput = (userinput)=>{

    let split_time = userinput.split('@');
    let split_pro  = split_time[0].split('*');

    let block_time = split_time[1]; // unformed time 
    let block_pro  = (split_pro[1]) ? split_pro[1] : 4; // Actual Priority
    let block_task = split_pro[0].split('#')[0]
    let time_blocks = [];
    time_blocks     = (block_time) ?  block_time.split(' ').filter(String) : [];
    let time_obj   = {}
    time_blocks.map( (t)=>{
       if(t.endsWith('m')){ time_obj.time = t; }
       if(t <= 31){ time_obj.day = t; }
       if(t.length == 3 && !t.endsWith('m')){ time_obj.month = t; }
       if(parseInt(t) && t.length == 4 && !t.endsWith('m')){ time_obj.year = t; }
    })
    let d = new Date()
    time_obj.day    = (time_obj.day) ? time_obj.day : d.getDate();
    time_obj.month  = (time_obj.month) ? get_month(time_obj.month) : d.getMonth()+1;
    time_obj.year   = (time_obj.year) ? time_obj.year : d.getFullYear();
    time_obj.time   = (time_obj.time) ? get_time(time_obj.time) : '23:59';
    let formatted_time = `${time_obj.year}-${time_obj.month}-${time_obj.day} ${time_obj.time}`;

    return {
        'name': block_task,
        'deadline' : formatted_time,
        'priority' : block_pro
    }
}

let get_month = (month)=>{
    let months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'];
    let index = 1;
    months.map( (m,i)=>{
        if(month.toUpperCase() == m.toUpperCase()){ index = i;}
    })
    return index+1;
}

let get_time  = (time)=>{
    time = (time == '12pm') ? '0pm' : time ;
    let format    = time.slice(-2);
    let time_num  = time.replace(/[^\d.]/g, '')
    let timeblock = (format == "pm") ? 12 : 0 ;
    let unformed_time = (parseFloat(time_num) + parseFloat(timeblock)).toFixed(2);
    let hour = parseInt(unformed_time);
    let minutes = unformed_time.substring(unformed_time.indexOf(".")+1, unformed_time.length);
    minutes = (minutes > 59 ) ? minutes % 60 : minutes;
    return `${hour}:${minutes}`;
}

let generate_template = (data)=>{

    let outlines = get_outlines()
    let outline = ''
    outlines.map((o)=>{
        if(o.id == data.outline_id){
            outline = o.name;
        }
    });
    let p = data.priority;
    let priority = (p == 1) ? 'Urgent' : ( p == 2) ? 'Important' : (p == 3) ? 'Moderate' : 'Not Important';
    let d = new Date()
    let is_overdue = (d > data.deadline) ? 'has-text-danger overdue ' : '';
    let dead = new Date(data.deadline)
    let readable = `${dead.toDateString()} ${dead.toLocaleTimeString()}`;
    
    let task_html = ` 
    <tr id="taskrow${data.id}">
    <td> 
        <button class="button is-small is-rounded is-danger" onclick="finishtask('${data.id}','False')">
           <span class="icon is-small">
                <i class="fas fa-check"></i>
           </span>
        </button>
    </td>
    <td class="task">
        <a class="">${data.name}</a>
        <h5 class="smalldate ${is_overdue}">
                ${readable}
        </h5>
    </td>
    <td><span class="tag is-light">${priority}</span></td>
    <td><span class="tag is-dark">${outline}</span></td>
    <td><p class="buttons">
            
            <button class="button is-small is-rounded finishtask" onclick="removetask('${data.id}')">
              <span class="icon is-small">
                  <i class="fas fa-times"></i>
              </span>
            </button>
        </p>    
    </tr> `;
    return task_html;
}

// let response = {
//                "status": "ok", 
//                "data": [
//                    {"id": 28,
//                     "name": "Adding a new task for today ",
//                     "deadline": "2020-01-03T18:00:00Z",
//                     "priority": 4, 
//                     "created_by_id": 1, 
//                     "created_at": "2020-01-03T12:13:48.502Z", 
//                     "closed_at": null, 
//                     "status": false, 
//                     "outline_id": 7
//                     }
//                 ]};
// let data = response.data[0];
// let html = generate_template(data)
// $('#tasklists').prepend(html)

function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();      
      reader.onload = function(e) {
        $('#previewimg').attr('src', e.target.result);
      }      
      reader.readAsDataURL(input.files[0]);
    }
}
  
$("#upimg").change(function() {
     readURL(this);
});

$("input[name=username]").keyup(function(){
     $("#uu").html('@'+$("input[name=username]").val())
})

$("input[name=email]").keyup(function(){
    $("#ee").html($("input[name=email]").val())
})


$("textarea[name=bio]").keyup(function(){
    $("#bb").html($("textarea[name=bio]").val())
});
