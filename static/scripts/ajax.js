function playMusic(type, id) {
    $.ajax({
        url: `/play-music/${type}/${id}`,
        type: "GET",
        dataType: "json",
        success: (data) => {
            $("#media").html(data.data)
        },
        error: (error) => {
            console.log(error);
        }
    });
}