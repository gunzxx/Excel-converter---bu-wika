// $(document).load()

$('.delete-btn').click(event => {
    event.preventDefault()
    
    const filename = event.target.dataset.filename.split('/').pop()
    console.log(filename);
    
    Swal.fire({
        title: "Hapus laporan?",
        text: "Yakin untuk menghapus laporan?",
        icon: "question",
        showCancelButton: true,
    }).then(res => {
        if (res.isConfirmed){
            axios.delete('/bulanan', {
                data: {
                    filename: filename,
                }
            }).then(apiRes=>{
                // console.log(apiRes);
                if (apiRes.status == 200){
                    Swal.fire({
                        text: "Laporan berhasil dihapus",
                        icon: "success",
                    }).then(res2 => {
                        document.location.reload()
                    })
                }
            }).catch(error => {
                Swal.fire({
                    text: error.response ? error.response.data.error : error.message,
                    icon: "error",
                }).then(res2 => {
                    document.location.reload()
                })
            })
        }
    })
})