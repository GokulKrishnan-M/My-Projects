
<?php $__env->startSection('content'); ?>

<br><br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">Subcategory Insert</h4>
                  <p class="card-description">
                    Insert your Category Information
                  </p>
                  <form  class="forms-sample"form  action="<?php echo e(route('subcatinsert')); ?>" method="post" enctype="multipart/form-data">
                     <?php echo csrf_field(); ?>
                      <div class="mb-4">
                      <label for="username" class="inline-block mb-2 ml-1 font-bold text-xs text-slate-700 dark:text-white/80">SUBCATEGORY NAME</label><br>
                      <select class="form-control" name="catid">
                      <option value="">-- Select Category Name --</option>
                       <?php $__currentLoopData = $subcat; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $d): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                        <option value="<?php echo e($d->catid); ?>">
                            <?php echo e($d->catname); ?>

                        </option>
                       <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                      </select>
                    </div>
                    <div class="form-group">
                      <label for="exampleInputName1"> CATEGORY NAME</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Name" name="subcatname">
                      <?php $__errorArgs = ['subcatname'];
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
                      <label for="exampleInputName1"> Image</label>
                      <input type="file" class="form-control"  placeholder="Name" name="subimage">
                      <?php $__errorArgs = ['subimage'];
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
<?php echo $__env->make('layouts.adminmaster', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Admin/subcategory.blade.php ENDPATH**/ ?>