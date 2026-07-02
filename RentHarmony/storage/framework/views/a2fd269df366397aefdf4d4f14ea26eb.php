
<?php $__env->startSection('content'); ?>

<br><br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">Location Insert</h4>
                  <p class="card-description">
                    Insert your Location name
                  </p>
                  <form  class="forms-sample"form  action="<?php echo e(route('location_insert')); ?>" method="post">
                     <?php echo csrf_field(); ?>
                      <div class="mb-4">
                      <label for="username" class="inline-block mb-2 ml-1 font-bold text-xs text-slate-700 dark:text-white/80">DISTRICT NAME</label><br>
                      <select class="form-control" name="districtid" id="districtid">
                      <option value="">-- Select District Name --</option>
                       <?php $__currentLoopData = $dist; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $d): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                        <option value="<?php echo e($d->districtid); ?>">
                            <?php echo e($d->districtname); ?>

                        </option>
                       <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                      </select>
                    </div>
                    <div class="form-group">
                      <label for="exampleInputName1"> LOCATION NAME</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Name" name="locationname">
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
<?php echo $__env->make('layouts.adminmaster', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Admin/location.blade.php ENDPATH**/ ?>