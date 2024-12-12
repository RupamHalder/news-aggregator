function showCommingSoon() {
    $.toast({
        heading: 'Comming soon...',
        text: 'This feature is comming soon.',
        icon: 'info',
        loader: true,        // Change it to false to disable loader
        loaderBg: '#9EC600',  // To change the background
        position: 'top-right',
    });
}