document.addEventListener('DOMContentLoaded', main);

function main() {
	// เข้าถึง html ผ่านทาง DOM
	const imageFile = document.getElementById('imageFile');
	const imageSrc = document.getElementById('imageSrc');
	const videoSrc = document.getElementById('videoSrc');
	const imageDes = document.getElementById('imageDes');
	const imageBefore = document.getElementById('imageBefore');
	const imageAfter = document.getElementById('imageAfter');
	const sendShape = document.getElementById('send_shape');
	const sendHough = document.getElementById('send_hough');
	const result = document.getElementById('result');

	const ctxBefore = imageBefore.getContext('2d');
	const ctxAfter = imageAfter.getContext('2d');

	const maxWidth = 800;
	const maxHeight = 600;

	let interval = null;

	imageFile.addEventListener('change', () => {
		const file = imageFile.files[0];
		console.log(`Selected file: ${file.name}, size: ${file.size} bytes`);
		if (file) {
			if (file.type.startsWith('video/')) {
				videoSrc.onloadedmetadata = function(event) {
					console.log("VID DATA:", videoSrc.videoWidth, videoSrc.videoHeight);
					let w,h;
					let width = videoSrc.videoWidth, height = videoSrc.videoHeight;
					if (width > height) {
						if (width < maxWidth) {
							w = width;
							h = height;
						} else {
							w = maxWidth;
							h = height * (maxWidth / width);
						}
					} else {
						if (height < maxHeight)
						{
							h = height;
							w = width;
						} else {
							h = maxHeight;
							w = width * (maxHeight / height);
						}
					}
					videoSrc.width = w;
					videoSrc.height = h;
					imageBefore.width = w;
					imageBefore.height = h;
					imageBefore.className = 'hide';
					videoSrc.className = "show";

					if (interval) clearInterval(interval);
					interval = setInterval(function() {
						ctxBefore.clearRect(0, 0, imageBefore.width, imageBefore.height);
						ctxBefore.drawImage(videoSrc, 0, 0, videoSrc.width, videoSrc.height);
						console.log("DRAW VID!", interval);
					}, 100);
				}
				videoSrc.src = URL.createObjectURL(file);
				videoSrc.play();
				return;
			}
			if (interval) clearInterval(interval);
			videoSrc.className = "hide";
			imageBefore.className = "show";
			const reader = new FileReader();
			reader.onload = function(event) {
				imageSrc.onload = function() {
					let w,h;
					let width = imageSrc.width, height = imageSrc.height;
					if (width > height) {
						if (width < maxWidth) {
							w = width;
							h = height;
						} else {
							w = maxWidth;
							h = height * (maxWidth / width);
						}
					} else {
						if (height < maxHeight)
						{
							h = height;
							w = width;
						} else {
							h = maxHeight;
							w = width * (maxHeight / height);
						}
					}
					imageBefore.width = w;
					imageBefore.height = h;
					ctxBefore.clearRect(0, 0, w, h);
					ctxBefore.drawImage(imageSrc, 0, 0, w, h);
				};
				imageSrc.src = event.target.result;
			}
			reader.readAsDataURL(file);
		}
	});

	sendShape.addEventListener('click', () => {
		console.log("Sending shape detection request...");
		sendClick('/wp1_backend_shape', {
			brightness: document.getElementById('p_brightness').value,
			blur: document.getElementById('p_blur').value,
			area: document.getElementById('p_area').value
		});
	});

	sendHough.addEventListener('click', () => {
		console.log("Sending Hough circle detection request...");
		sendClick('/wp1_backend_hough', {
			blur: document.getElementById('h_blur').value,
			minDist: document.getElementById('h_dist').value,
			param1: document.getElementById('h_param1').value,
			param2: document.getElementById('h_param2').value,
			minRadius: document.getElementById('h_min_r').value,
			maxRadius: document.getElementById('h_max_r').value,
		});
	});

	function sendClick(backendUrl, parameters) {
		const data = {
			imageBASE64: imageBefore.toDataURL('image/png').split(',')[1],
			type: 'image/png',
			width: imageBefore.width,
			height: imageBefore.height,
			parameters: parameters
		};
		console.log(`Sending data to backend: `, data);
		fetch(backendUrl, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		})
		.then(response => response.json())
		.then(data => {
			console.log(`Received data from backend: `, data);
			imageDes.onload = function() {
				let w, h;
				w = data.image.width;
				h = data.image.height;
				imageAfter.width = w;
				imageAfter.height = h;
				ctxAfter.clearRect(0, 0, w, h);
				ctxAfter.drawImage(imageDes, 0, 0, w, h);
			}
			imageDes.src = `data:${data.image.type};base64,${data.image.imageBASE64}`;
			result.innerHTML = `จำนวนเหรียญที่ตรวจพบ: ${data.coins}`;
		});
	}
}