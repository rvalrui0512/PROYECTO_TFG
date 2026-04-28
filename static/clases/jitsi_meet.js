document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('jitsi-meet-container');
  const statusBox = document.getElementById('jitsi-status');

  if (!container) {
    return;
  }

  if (typeof JitsiMeetExternalAPI === 'undefined') {
    if (statusBox) {
      statusBox.className = 'alert alert-danger mb-3';
      statusBox.textContent = 'No se pudo cargar Jitsi Meet.';
    }
    return;
  }

  const roomName = container.dataset.roomName;
  const displayName = container.dataset.displayName || '';
  const domain = container.dataset.jitsiDomain || 'meet.jit.si';
  const returnUrl = container.dataset.returnUrl || '';

  if (!roomName) {
    if (statusBox) {
      statusBox.className = 'alert alert-danger mb-3';
      statusBox.textContent = 'No se pudo inicializar la sala privada.';
    }
    return;
  }

  if (statusBox) {
    statusBox.className = 'alert alert-info mb-3';
    statusBox.textContent = 'Conectando con la sala privada...';
  }

  const api = new JitsiMeetExternalAPI(domain, {
    roomName,
    parentNode: container,
    width: '100%',
    height: '100%',
    userInfo: {
      displayName,
    },
    configOverwrite: {
      prejoinPageEnabled: false,
      disableDeepLinking: true,
      startWithAudioMuted: false,
      startWithVideoMuted: false,
    },
    interfaceConfigOverwrite: {
      TOOLBAR_BUTTONS: [
        'microphone',
        'camera',
        'chat',
        'desktop',
        'fullscreen',
        'hangup',
        'raisehand',
        'tileview',
        'settings',
      ],
    },
  });

  window.jitsiMeetApi = api;

  api.addListener('videoConferenceJoined', () => {
    if (statusBox) {
      statusBox.className = 'alert alert-success mb-3';
      statusBox.textContent = 'Has entrado en la videollamada privada.';
    }
  });

  api.addListener('videoConferenceLeft', () => {
    if (statusBox) {
      statusBox.className = 'alert alert-secondary mb-3';
      statusBox.textContent = 'Has salido de la videollamada.';
    }
    if (returnUrl) {
      window.location.replace(returnUrl);
    }
  });

  api.addListener('readyToClose', () => {
    if (statusBox) {
      statusBox.className = 'alert alert-secondary mb-3';
      statusBox.textContent = 'La sala se ha cerrado.';
    }
    if (returnUrl) {
      window.location.replace(returnUrl);
    }
  });
});