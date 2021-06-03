document.querySelector("#realcontent").style.opacity = "1"
document.querySelector("#logo").style.opacity = "0"
var voter = {
	vote: function (id, side, element) {
		document.querySelector("#realcontent").style.opacity = "0"
		document.querySelector("#logo").style.opacity = "1"
		fetch('https://would-you-rather.ch1ck3n.repl.co/api/question/vote?id=' + id + "&side=" + side)
			.then(
				function (response) {
					if (response.status !== 200) {
						console.log('Looks like there was a problem. Status Code: ' +
							response.status);
						return;
					}

					// Examine the text in the response
					response.json().then(function (data) {
						document.querySelector("#realcontent").style.opacity = "1"
						document.querySelector("#logo").style.opacity = "0"
            console.log(data.data)
						if (data.status == "true") {
							element.parentNode.innerHTML = "<div class=\"red box\" onClick=\"voter.vote({{ question.id }}, \'left\', this)\"><span>" + data.data.vt_l + "%<\/span><br><span style=\"font-size: 90%;\">" + data.data.left + "</span><br><hr><span style=\"font-size: 120%;\">" + data.data.vt_l2 + " votes</span><\/div>&nbsp&nbsp&nbsp&nbsp    \r\n    <div class=\"blue box\" onClick=\"voter.vote({{ question.id }}, \'right\', this)\"><span>" + data.data.vt_r + "%<\/span><br><span style=\"font-size: 90%;\">" + data.data.right + "</span><br><hr><span style=\"font-size: 120%;\">" + data.data.vt_r2 + "</span> votes<\/div>"
						}
						if (data.status == "false") {
							element.parentNode.innerHTML = "<div class=\"red box\" onClick=\"voter.vote({{ question.id }}, \'left\', this)\"><span>" + data.data.vt_l + "%<\/span><br><span style=\"font-size: 90%;\">" + data.data.left + "</span><br><hr><span style=\"font-size: 120%;\">" + data.data.vt_l2 + " votes</span><\/div>&nbsp&nbsp&nbsp&nbsp    \r\n    <div class=\"blue box\" onClick=\"voter.vote({{ question.id }}, \'right\', this)\"><span>" + data.data.vt_r + "%<\/span><br><span style=\"font-size: 90%;\">" + data.data.right + "</span><br><hr><span style=\"font-size: 120%;\">" + data.data.vt_r2 + "</span> votes<\/div>"
						}
					});
				}
			)
			.catch(function (err) {
				console.log('Fetch Error :-S', err);
			});
	},
	random: function (element) {
		document.querySelector("#realcontent").style.opacity = 0
		document.querySelector("#logo").style.opacity = 1
		fetch('https://would-you-rather.ch1ck3n.repl.co/api/question/random')
			.then(
				function (response) {
					if (response.status !== 200) {
						console.log('Looks like there was a problem. Status Code: ' +
							response.status);
						return;
					}

					// Examine the text in the response
					response.json().then(function (data) {
						  document.querySelector("#realcontent").style.opacity = "1"
						  document.querySelector("#logo").style.opacity = "0"
              document.querySelector("#q_owner").innerHTML = "@" + (data.owner)
              document.querySelector("#pub_date").innerHTML = data.pub_data
              document.querySelector("#q_owner").href = "@" + (data.owner)
							element.parentNode.childNodes[1].innerHTML = "    <div class=\"red box\" onClick=\"voter.vote("+data.id+", \'left\', this)\"><span>"+data.left+"<\/span><\/div>&nbsp&nbsp&nbsp&nbsp\r\n    <div class=\"blue box\" onClick=\"voter.vote("+data.id+", \'right\', this)\"><span>"+data.right+"<\/span><\/div>"
					});
				}
			)
			.catch(function (err) {
				console.log('Fetch Error :-S', err);
			});
	}
}