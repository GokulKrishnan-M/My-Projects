
<?php $__env->startSection('content'); ?>

<br><br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">District Insert</h4>
                  <p class="card-description">
                    Insert your district name
                  </p>
                  <form  class="forms-sample"form  action="<?php echo e(route('updatedisttable',$dist->districtid)); ?>" method="post">
                     <?php echo csrf_field(); ?>
                    <div class="form-group">
                      <label for="exampleInputName1"> District Name</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Name" name="districtname" value="<?php echo e($dist->districtname); ?>">
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
<?php echo $__env->make('layouts.adminmaster', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Admin/updatedist.blade.php ENDPATH**/ ?>