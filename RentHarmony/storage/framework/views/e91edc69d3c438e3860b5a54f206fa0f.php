
<?php $__env->startSection('content'); ?>


<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<script>
    $(document).ready(function () {
        // When category is changed
        $('#catid').change(function () {
            var catid = $(this).val();
            if (catid) {
                $.ajax({
                    url: '/getsubcatid/' + catid,
                    type: 'GET',
                    success: function (data) {
                        $('#subcategory').empty().append('<option value="">Choose Subcategory</option>');
                        $('#instrument').empty();
                        $.each(data, function (key, value) {
                            $('#subcategory').append(
                                '<option value="' + value.subcatid + '">' + value.subcatname + '</option>'
                            );
                        });
                    }
                });
            } else {
                $('#subcategory').empty();
                $('#instrument').empty();
            }
        });

        // When subcategory is changed
        $('#subcategory').change(function () {
            var subcategoryId = $(this).val();
            if (subcategoryId) {
                $.ajax({
                    url: '/getinst/' + subcategoryId,
                    type: 'GET',
                    success: function (data) {
                        $('#instrument').empty();
                        let i = 1;
                        $.each(data, function (key, value) {
                            $('#instrument').append(
                                '<tr>' +
                                    '<td>' + i++ + '</td>' +
                                    '<td>' + value.instname + '</td>' +
                                    '<td><img src="/uploads/' + value.image +'"></td>' +
                                    '<td>' + value.desc + '</td>' +
                                    '<td>' + value.ppd + '</td>' +
                                    '<td>' + value.stock + '</td>' +
                                    '<td>' + value.status + '</td>' +
                                     '<td><a href="/deleteinst/' + value.instid + '" onclick="return confirm(\'Are you sure you want to delete this subcategory?\')">' +
                                    '<button class="btn btn-danger btn-sm">Delete</button></td>' +
                                    '</a>' +
                                    '<td><a href="/updateinst/' + value.instid + '" onclick="return confirm(\'Are you sure you want to edit this subcategory?\')">' +
                                    '<button class="btn btn-primary btn-sm">Edit</button></td>' +
                                    '</a>' +
                                '</tr>'
                            );
                        });
                    }
                });
            } else {
                $('#instrument').empty();
            }
        });
    });
</script>

<div class="col-lg-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">Striped Table</h4>
                  <p class="card-description">
                    Add class <code>.table-striped</code>
                  </p>
                   <label for="username" class="inline-block mb-2 ml-1 font-bold text-xs text-slate-700 dark:text-white/80">CATEGORY NAME</label><br>
                      <select class="form-control" name="catid" id="catid">
                      <option value="">-- Select category Name --</option>
                       <?php $__currentLoopData = $cat; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $d): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                        <option value="<?php echo e($d->catid); ?>">
                            <?php echo e($d->catname); ?>

                        </option>
                       <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                      </select><br><br>

 <div class="form-group">
                       <label for="subcategoryid">Subcategory</label>
                       <select name="subcategoryid" id="subcategory" required class="form-control">
                           <option value="">Select a subcategory</option>
                       </select>
                        </div><br><br>

                  <div class="table-responsive">
                    <table class="table table-striped">
                      <thead>
                        <tr>
                          <th>
                            SI.
                          </th>
                          <th>
                            INSTRUMENT NAME
                          </th>
                          <th>
                            IMAGE
                          </th>
                          <th>
                            DESCRIPTION
                          </th>
                          <th>
                            PRICE PER DAY
                          </th>
                          <th>
                            STOCK
                          </th>
                          <th>
                            STATUS
                          </th>
                           <th>
                            DELETE
                          </th>
                           <th>
                            UPDATE
                          </th>
                        </tr>
                      </thead>
                      <tbody id="instrument">
                         <?php $__currentLoopData = $inst; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $index => $d): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                            <tr>
                                <td><?php echo e($index + 1); ?></td>
                                <td><?php echo e($d->instname); ?></td>
                                <td><img src="<?php echo e(asset('/uploads/' . $d->image)); ?>" class="h-20 w-20 object-cover rounded shadow" alt="Image" 
 style="height: 100px;width:100px;"></td>
                                <td><?php echo e($d->desc); ?></td>
                                <td><?php echo e($d->ppd); ?></td>
                                <td><?php echo e($d->stock); ?></td>
                                <td><?php echo e($d->status); ?></td>
                                <td>
                                    <a href="<?php echo e(route('deleteinst' , ['instid' => $d->instid])); ?>" class="btn btn-sm btn-danger" onclick="return confirm('Are you sure you want to delete this Department?')">Delete</a>
                                </td>
                                <td>
                                    <a href="<?php echo e(route('updateinst' , ['instid' => $d->instid])); ?>" class="btn btn-sm btn-primary" >Edit</a>
                                </td>
                            </tr>
                        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                      </tbody>
                    </table>
                     <?php if(session('success')): ?>
                  <script>
                    alert('<?php echo e(session('success')); ?>')
                  </script>
                  <?php endif; ?>
                  </div>
                </div>
              </div>
            </div>
</div>
</div>

            <?php $__env->stopSection(); ?>
<?php echo $__env->make('layouts.adminmaster', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Admin/instrumentview.blade.php ENDPATH**/ ?>