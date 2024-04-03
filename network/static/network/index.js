document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit-form').forEach((form) => {
        form.style.display = 'none' 
    })

    document.querySelectorAll('.edit-button').forEach((button) => {
        button.onclick = () => {
            const clicked_post = button.parentNode
            // console.log(button.parentNode.id)
            // console.log(button.parentNode.querySelector('.content'))
            clicked_post.querySelector('.edit-form').style.display = 'block'
            clicked_post.querySelector('.content').style.display = 'none'
        }
    })

    document.querySelectorAll('#submit-button').forEach((button) => {
        button.onclick = () => {
            post = button.parentNode.parentNode
            fetch(`/posts/${post.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    content: post.querySelector('textarea').value
                })
            })
            .then(() => {
                fetch(`/posts/${post.id}`)
                .then(response => response.json())
                .then(get_post => {
                    post.querySelector('.content').innerHTML = get_post.content
                })
            })
            post.querySelector('.edit-form').style.display = 'none'
            post.querySelector('.content').style.display = 'block'
            console.log(post.querySelector('textarea').innerHTML)
            
        }
    })
})