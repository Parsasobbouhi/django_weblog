function like(slug, id) {
    var element = document.querySelector(`i[data-article-id="${id}"]`);
    var count = document.querySelector(`.like-count[data-article-id="${id}"]`);

    $.get(`/articles/like/${slug}/${id}`).then(response => {
        if (response['response'] === "liked") {
            element.className = "fa fa-heart";
            count.innerText = Number(count.innerText) + 1;
        } else {
            element.className = "fa fa-heart-o";
            count.innerText = Number(count.innerText) - 1;
        }
    });
}

function submitContactForm() {
    var form = document.getElementById('contact-form');
    var formData = new FormData(form);
    var url = form.action;

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        var messageContainer = document.getElementById('form-message');


        if (data.success) {
            messageContainer.innerHTML = `
                <div class="alert alert-success">
                    Your message has been sent. Go to 
                    <a href="/">main page</a>.
                </div>`;
            form.reset();
        } else {
            messageContainer.innerHTML = `
                <div class="alert alert-danger">
                    Please correct the errors and try again.
                </div>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        var messageContainer = document.getElementById('form-message');
        messageContainer.innerHTML = `
            <div class="alert alert-danger">
                Something went wrong. Please try again.
            </div>`;
    });
}

document.getElementById('contact-form').onsubmit = function(e) {
    e.preventDefault();
    submitContactForm();
};

function submitComment() {
    $('#comment').submit(function (e) {
        e.preventDefault();

        var formData = $(this).serialize();
        var url = window.location.href;

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function (response) {
                $('#comments-section ul').append(response.comment_html);
                $('#comment')[0].reset();
                $('#parent_id').val('');
                $('#cancel-reply').hide();
            },
            error: function () {
                alert('Something went wrong. Please try again.');
            }
        });
    });
}




