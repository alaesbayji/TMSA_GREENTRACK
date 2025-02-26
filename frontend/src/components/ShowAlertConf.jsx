import Swal from 'sweetalert2';

const ShowAlertConf = (type, message, options = {}) => {
    if (type === "warning" && options.showCancelButton) {
      // Exemple avec une bibliothèque comme SweetAlert2
      Swal.fire({
        title: message,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: options.confirmButtonText || "Confirm",
        cancelButtonText: options.cancelButtonText || "Cancel",
      }).then((result) => {
        if (result.isConfirmed) {
          options.onConfirm?.();
        } else {
          options.onCancel?.();
        }
      });
    } else {
      // Pour les autres types d'alertes
      Swal.fire({
        title: message,
        icon: type,
      });
    }
  };
  export default ShowAlertConf;