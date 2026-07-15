program precision_blas_real16_test
  implicit none

  complex :: cx(5), cy(5), dot
  complex :: cdotc, cdotu
  real :: sx(5), sy(5), sum
  real :: scasum
  integer :: icamax

  sx = [1.0, 2.0, 3.0, 4.0, 5.0]
  sy = 0.0
  call scopy(3, sx, -2, sy, 2)
  call require(all(sy == [5.0, 0.0, 3.0, 0.0, 1.0]), &
               'SCOPY reverse/strided')

  call sscal(3, 2.0, sx, 2)
  call require(all(sx == [2.0, 2.0, 6.0, 4.0, 10.0]), &
               'SSCAL strided')
  call sscal(3, 0.5, sx, -2)
  call require(all(sx == [1.0, 2.0, 3.0, 4.0, 5.0]), &
               'SSCAL reverse')

  cx = [(1.0, 2.0), (3.0, -1.0), (-2.0, 4.0), &
        (5.0, 0.0), (7.0, -3.0)]
  cy = (0.0, 0.0)
  call ccopy(3, cx, -2, cy, 2)
  call require(all(cy == [(7.0, -3.0), (0.0, 0.0), (-2.0, 4.0), &
                          (0.0, 0.0), (1.0, 2.0)]), &
               'CCOPY reverse/strided')

  call cscal(3, (2.0, -1.0), cx, 2)
  call require(all(cx == [(4.0, 3.0), (3.0, -1.0), (0.0, 10.0), &
                          (5.0, 0.0), (11.0, -13.0)]), &
               'CSCAL strided')

  cy = [(1.0, 0.0), (2.0, 0.0), (3.0, 0.0), &
        (4.0, 0.0), (5.0, 0.0)]
  call caxpy(3, (1.0, 0.0), cx, -2, cy, 2)
  call require(all(cy == [(12.0, -13.0), (2.0, 0.0), (3.0, 10.0), &
                          (4.0, 0.0), (9.0, 3.0)]), &
               'CAXPY reverse/strided')

  cx(1:2) = [(1.0, 2.0), (3.0, 4.0)]
  cy(1:2) = [(5.0, 6.0), (7.0, 8.0)]
  dot = cdotc(2, cx, 1, cy, 1)
  call require(dot == (70.0, -8.0), 'CDOTC')
  dot = cdotu(2, cx, 1, cy, 1)
  call require(dot == (-18.0, 68.0), 'CDOTU')

  sum = scasum(2, cx, 1)
  call require(sum == 10.0, 'SCASUM')
  call require(icamax(2, cx, 1) == 2, 'ICAMAX')
  call require(scasum(0, cx, 1) == 0.0, 'SCASUM empty')
  call require(icamax(0, cx, 1) == 0, 'ICAMAX empty')

  print '(A)', 'precision_blas_real16: PASS'

contains

  subroutine require(condition, label)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: label

    if (.not. condition) then
      write (*, '(A,A)') 'precision_blas_real16: FAIL: ', label
      error stop 1
    end if
  end subroutine require

end program precision_blas_real16_test
