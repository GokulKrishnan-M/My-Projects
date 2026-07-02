
<?php $__env->startSection('content'); ?>

<!-- Include jQuery -->
<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>

<!-- AJAX Script to Fetch Subcategories Based on Category -->
<script>
    $(document).ready(function () {
        $('#catid').change(function () {
            var catid = $(this).val();
            if (catid) {
                $.ajax({
                    url: '/getsubcatid/' + catid,
                    type: 'GET',
                    success: function (data) {
                        $('#subcategory').empty();
                        $('#subcategory').append('<option value="">Select a Subcategory</option>');
                        $.each(data, function (key, value) {
                            $('#subcategory').append('<option value="' + value.subcatid + '">' + value.subcatname + '</option>');
                        });
                    },
                    error: function () {
                        alert('Unable to fetch subcategories. Please try again later.');
                    }
                });
            } else {
                $('#subcategory').empty().append('<option value="">Select a Subcategory</option>');
            }
        });
    });
</script>

<br><br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">District Insert</h4>
                  <p class="card-description">
                    Instrument Details
                  </p>
                  <form  class="forms-sample" action="<?php echo e(route('instinsert')); ?>" method="post" enctype="multipart/form-data">
                     <?php echo csrf_field(); ?>
                    <div class="mb-4">
                      <label for="username" class="inline-block mb-2 ml-1 font-bold text-xs text-slate-700 dark:text-white/80">SUBCATEGORY NAME</label><br>
                      <select class="form-control" name="catid" id="catid">
                      <option value="">-- Select Category Name --</option>
                       <?php $__currentLoopData = $inst; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $d): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                        <option value="<?php echo e($d->catid); ?>">
                            <?php echo e($d->catname); ?>

                        </option>
                       <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                      </select>
                    </div>

                                       <div class="form-group">
                       <label for="subcategoryid">Subcategory</label>
                       <select name="subcategoryid" id="subcategory" required class="form-control">
                           <option value="">Select a subcategory</option>
                       </select>
                        </div>

                    <div class="form-group">
                      <label for="exampleInputName1"> Instrument Name</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Name" name="instname">
                      <?php $__errorArgs = ['instname'];
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
                      <label for="exampleInputName1">Instrument Image</label>
                      <input type="file" class="form-control" id="exampleInputName1" name="image">
                      <?php $__errorArgs = ['image'];
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
                      <label for="exampleInputName1">Desciption</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Description" name="desc">
                      <?php $__errorArgs = ['desc'];
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
                      <label for="exampleInputName1">Price Per Day</label>
                      <input type="number" class="form-control" id="exampleInputName1" placeholder="Price Per Day" name="ppd">
                      <?php $__errorArgs = ['ppd'];
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
                      <label for="exampleInputName1">Stock</label>
                      <input type="number" class="form-control" id="exampleInputName1" placeholder="Stock" name="stock">
                      <?php $__errorArgs = ['stock'];
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

                    
                    <button type="submit" class="btn btn-primary mr-2">Submit</button>
                   
                  </form>
                   <?php if(session('success')): ?>
                  <script>
                    alert('<?php echo e(session('success')); ?>')
                  </script>
                  <?php endif; ?>
                </div>
              </div>
            </div>

            <?php $__env->stopSection(); ?>
<?php echo $__env->make('layouts.adminmaster', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Admin/instrument.blade.php ENDPATH**/ ?>