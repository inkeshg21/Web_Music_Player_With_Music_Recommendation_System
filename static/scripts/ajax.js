function playMusic(id) {
    $.ajax({
        url: `/play-music/${id}`,
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