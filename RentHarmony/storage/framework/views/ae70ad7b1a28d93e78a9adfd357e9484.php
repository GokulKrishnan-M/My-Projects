
<?php $__env->startSection('content'); ?>

<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>

<!-- AJAX Script to Fetch Subcategories Based on Category -->
<script>
    $(document).ready(function () {
        $('#districtid').change(function () {
            var districtid = $(this).val();
            if (districtid) {
                $.ajax({
                    url: '/getloc/' + districtid,
                    type: 'GET',
                    success: function (data) {
                        $('#location').empty();
                        $('#location').append('<option value="">Select a location</option>');
                        $.each(data, function (key, value) {
                            $('#location').append('<option value="' + value.locationid + '">' + value.locationname + '</option>');
                        });
                    },
                    error: function () {
                        alert('Unable to fetch location. Please try again later.');
                    }
                });
            } else {
                $('#location').empty().append('<option value="">Select a location</option>');
            }
        });
    });
</script>

<style>
.card-registration .select-input.form-control[readonly]:not([disabled]) {
font-size: 1rem;
line-height: 2.15;
padding-left: .75em;
padding-right: .75em;
}
.card-registration .select-arrow {
top: 13px;
}
</style>
<section class="h-100 bg-dark">
  <div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col">
        <div class="card card-registration my-4">
          <div class="row g-0">
            <div class="col-xl-6 d-none d-xl-block">
              <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-registration/img4.webp"
                alt="Sample photo" class="img-fluid"
                style="border-top-left-radius: .25rem; border-bottom-left-radius: .25rem; height:100%" />
            </div>
             
            <div class="col-xl-6">
              <div class="card-body p-md-5 text-black">
                <form  class="forms-sample" action="<?php echo e(route('custinsert')); ?>" method="post">
                     <?php echo csrf_field(); ?>
                <h3 class="mb-5 text-uppercase">Student registration form</h3>

                <label class="form-label" for="form3Example8">CUSTOMER NAME</label>   
                <div data-mdb-input-init class="form-outline mb-4">
                  <input type="text" id="form3Example8" class="form-control form-control-lg" name="custname" />
                  <?php $__errorArgs = ['custname'];
$__bag = $errors->getBag($__errorArgs[1] ?? 'default');
if ($__bag->has($__errorArgs[0])) :
if (isset($message)) { $__messageOriginal = $message; }
$message = $__bag->first($__errorArgs[0]); ?>
                                <span class="error-message"><?php echo e($message); ?></span>
                            <?php unset($message);
if (isset($__messageOriginal)) { $message = $__messageOriginal; }
endif;
unset($__errorArgs, $__bag); ?>

                </div>

                <label class="form-label" for="form3Example8">E-MAIL</label>   
                <div data-mdb-input-init class="form-outline mb-4">
                  <input type="email" id="form3Example8" class="form-control form-control-lg" name="email"/>
                  <?php $__errorArgs = ['email'];
$__bag = $errors->getBag($__errorArgs[1] ?? 'default');
if ($__bag->has($__errorArgs[0])) :
if (isset($message)) { $__messageOriginal = $message; }
$message = $__bag->first($__errorArgs[0]); ?>
                                <span class="error-message"><?php echo e($message); ?></span>
                            <?php unset($message);
if (isset($__messageOriginal)) { $message = $__messageOriginal; }
endif;
unset($__errorArgs, $__bag); ?>
                </div>

                <label class="form-label" for="form3Example8">CONTACT NO</label>   
                <div data-mdb-input-init class="form-outline mb-4">
                  <input type="number" id="form3Example8" class="form-control form-control-lg" name="contno"/>
                  <?php $__errorArgs = ['contno'];
$__bag = $errors->getBag($__errorArgs[1] ?? 'default');
if ($__bag->has($__errorArgs[0])) :
if (isset($message)) { $__messageOriginal = $message; }
$message = $__bag->first($__errorArgs[0]); ?>
                                <span class="error-message"><?php echo e($message); ?></span>
                            <?php unset($message);
if (isset($__messageOriginal)) { $message = $__messageOriginal; }
endif;
unset($__errorArgs, $__bag); ?>
                </div>

                                <div class="form-group">
                    <label for="districtid">District</label>
                    <select name="districtid" id="districtid" required class="form-control">
                        <option value="">Select a district</option>
                        <?php $__currentLoopData = $dist; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $district): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                            <option value="<?php echo e($district->districtid); ?>"><?php echo e($district->districtname); ?></option>
                        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                    </select>
                </div>


                                <div class="form-group">
                    <label for="location">Location</label>
                    <select name="locationid" id="location" required class="form-control">
                        <option value="">Select a Location</option>
                    </select>
                </div>

                <label class="form-label" for="form3Example8">ADDRESS</label>   
                <div data-mdb-input-init class="form-outline mb-4">
                  <input type="text" id="form3Example8" class="form-control form-control-lg" name="address"/>
                </div>

                <label class="form-label" for="form3Example8">USERNAME</label>   
                <div data-mdb-input-init class="form-outline mb-4">
                  <input type="text" id="form3Example8" class="form-control form-control-lg" name="username"/>
                  <?php $__errorArgs = ['username'];
$__bag = $errors->getBag($__errorArgs[1] ?? 'default');
if ($__bag->has($__errorArgs[0])) :
if (isset($message)) { $__messageOriginal = $message; }
$message = $__bag->first($__errorArgs[0]); ?>
                                <span class="error-message"><?php echo e($message); ?></span>
                            <?php unset($message);
if (isset($__messageOriginal)) { $message = $__messageOriginal; }
endif;
unset($__errorArgs, $__bag); ?>
                </div>
                
                <label class="form-label" for="form3Example8">PASSWORD</label>   
                <div data-mdb-input-init class="form-outline mb-4">
                  <input type="password" id="form3Example8" class="form-control form-control-lg" name="password"/>
                  <?php $__errorArgs = ['password'];
$__bag = $errors->getBag($__errorArgs[1] ?? 'default');
if ($__bag->has($__errorArgs[0])) :
if (isset($message)) { $__messageOriginal = $message; }
$message = $__bag->first($__errorArgs[0]); ?>
                                <span class="error-message"><?php echo e($message); ?></span>
                            <?php unset($message);
if (isset($__messageOriginal)) { $message = $__messageOriginal; }
endif;
unset($__errorArgs, $__bag); ?>
                </div>

                <div class="d-flex justify-content-end pt-3" >
                 <div style="padding-right:30px"> <button  type="button" data-mdb-button-init data-mdb-ripple-init class="btn btn-light btn-lg" >Reset all</button> </div> 
                  <div><button  type="submit" data-mdb-button-init data-mdb-ripple-init class="btn btn-warning btn-lg ms-2">Submit form</button></div>
                </div>

              </div>
            </div>
</form>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
 <?php $__env->stopSection(); ?>
<?php echo $__env->make('layouts.guestmaster', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Guest/customerreg.blade.php ENDPATH**/ ?>