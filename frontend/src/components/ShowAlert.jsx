import Swal from 'sweetalert2';

const ShowAlert = (type, message) => {
  switch (type) {
    case 'success':
      return Swal.fire({
        icon: 'success',
        title: 'Succès',
        text: message,
        confirmButtonColor: '#3085d6',
      });
    case 'error':
      return Swal.fire({
        icon: 'error',
        title: 'Erreur',
        text: message,
        confirmButtonColor: '#d33',
      });
    case 'confirmation':
      return Swal.fire({
        title: 'Êtes-vous sûr ?',
        text: message,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Oui',
        cancelButtonText: 'Annuler',
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
            icon: 'success',
            title: 'Confirmé',
            text: 'Action confirmée avec succès !',
          });
        }
      });
    default:
      return Swal.fire({
        icon: 'info',
        title: 'Info',
        text: message || 'Ceci est une alerte par défaut.',
        confirmButtonColor: '#3085d6',
      });
  }
};

export default ShowAlert;