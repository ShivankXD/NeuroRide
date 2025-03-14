window.addEventListener('DOMContentLoaded', event => {
    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink');
        } else {
            navbarCollapsible.classList.add('navbar-shrink');
        }
    };
    navbarShrink();
    document.addEventListener('scroll', navbarShrink);

    // ScrollSpy
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    }

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Analyze Section Functionality
    const uploadPhotoBtn = document.getElementById('uploadPhotoBtn');
    const uploadVideoBtn = document.getElementById('uploadVideoBtn');
    const liveVideoBtn = document.getElementById('liveVideoBtn');
    const fileInput = document.getElementById('fileInput');
    const uploadedImage = document.getElementById('uploadedImage');
    const uploadedVideo = document.getElementById('uploadedVideo');
    const uploadedMediaContainer = document.getElementById('uploadedMediaContainer');
    const scanOverlay = document.getElementById('scanOverlay');
    const analysisResult = document.getElementById('analysisResult');
    const numberPlateResult = document.getElementById('numberPlateResult');
    const downloadExcelBtn = document.getElementById('downloadExcelBtn');

    // Handle Photo Upload Button Click
    uploadPhotoBtn.addEventListener('click', () => {
        fileInput.accept = 'image/*';
        fileInput.click();
    });

    // Handle Video Upload Button Click
    uploadVideoBtn.addEventListener('click', () => {
        fileInput.accept = 'video/*';
        fileInput.click();
    });

    // Handle Live Video Button Click (Coming Soon)
    liveVideoBtn.addEventListener('click', () => {
        alert('Live Video feature is coming soon!');
    });

    // Handle File Input Change
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            // Show loading state
            scanOverlay.style.display = 'block';
            analysisResult.style.display = 'none';

            // Send the file to the Flask backend
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Clear previous results
                    uploadedImage.style.display = 'none';
                    uploadedVideo.style.display = 'none';

                    // Display the uploaded media
                    if (data.file_type === 'image') {
                        uploadedImage.src = URL.createObjectURL(file);
                        uploadedImage.style.display = 'block';
                    } else if (data.file_type === 'video') {
                        uploadedVideo.src = URL.createObjectURL(file);
                        uploadedVideo.style.display = 'block';
                    }
                    uploadedMediaContainer.style.display = 'block';

                    // Simulate scanning (optional)
                    setTimeout(() => {
                        scanOverlay.style.display = 'none';
                        analysisResult.style.display = 'block';
                        if (data.number_plate) {
                            numberPlateResult.textContent = data.number_plate;
                        } else {
                            numberPlateResult.textContent = data.message;
                        }
                    }, 5000); // Simulate 5 seconds of scanning
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while uploading the file.');
            });
        }
    });

// Handle Download Excel Button Click
downloadExcelBtn.addEventListener('click', () => {
    // Trigger the download
    fetch('/download_excel')
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || 'Failed to download Excel file.');
                });
            }
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'analysis_results.xlsx';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message || 'An error occurred while downloading the Excel file.');
        });
});
});