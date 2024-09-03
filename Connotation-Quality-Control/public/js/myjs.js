document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];

    if (file && file.name.endsWith('.docx')) {
        // 读取 .docx 文件内容
        readDocxFile(file);
    } else {
        alert('Please select a valid .docx file.');
    }
});

function readDocxFile(file) {
    const reader = new FileReader();

    reader.onload = function(event) {
        const arrayBuffer = event.target.result;

        var docData = arrayBuffer;

        docx.renderAsync(docData, document.getElementById("preview")).then(x => console.log("docx: finished"));
        // 显示文档内容
        document.getElementById('preview').innerText = content;
    };

    reader.readAsArrayBuffer(file);
}




var g_qrcode = undefined;



// 图片预览
$(document).ready(function () {

     $('#loading').hide();

    $('#submitBtn').click(function() {
         $('#loading').addClass('active');
         $('#loading').show();
        var formData = new FormData($('#uploadForm')[0]);

        $.ajax({
            url: '/upload_term',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                console.log(response);
                 $('#loading').hide();
                 if(response.code == 0){
                     window.location.href = '../doc_res?id=' + response.data.id;
                 }else{
                     $('#errorModal').modal('show');
                 }

                // 在这里处理响应，可以根据需要进行页面跳转或其他操作
            },
            error: function(error) {
                console.error(error);
                $('#loading').hide();
                $('#errorModal').modal('show');
            }
        });
    });


});

function enterStep(step){
    window.location.href = `/index_step_${step}/?qrcode=${g_qrcode}`;
}