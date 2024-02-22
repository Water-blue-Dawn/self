#include <opencv2/opencv.hpp>
#include <iostream>
using namespace cv;
using namespace std;

int main()
{
	Mat frame;
	VideoCapture input;
	input.open("v2.avi");
	if (!input.isOpened())
	{
		cout << "读取出错" << endl;
		return -1;
	}
	while (input.read(frame))
	{
		Scalar color = frame.at<Vec3b>(150, 150);
		Mat grey;
		vector<Mat>channels;
		split(frame, channels);
		//灰度图
		grey = channels.at(2) - channels.at(0);
		//阈值化
		Mat bin;
		threshold(grey, bin, 125, 255, THRESH_BINARY);
		//膨胀 (加上膨胀出现卡顿，效果不是很明显)
		Mat element = getStructuringElement(MORPH_RECT, Size(2, 2));
		Mat out;
		dilate(bin, out, element);
		//
		vector<vector<Point>> contour;
		vector<Vec4i> hierarchy;
		findContours(bin, contour, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_TC89_KCOS);
		vector<vector<Point>> conPoly(contour.size());
		vector<Rect> boundRect(contour.size());

		for (int i = 0; i < contour.size(); i++) {
			int area = contourArea(contour[i]);
			//cout << area << endl;
			if (area < 300 and area>10) {
				float peri = arcLength(contour[i], true);
				approxPolyDP(contour[i], conPoly[i], 0.02 * peri, true);//把一个连续光滑曲线折线化
				boundRect[i] = boundingRect(conPoly[i]);
				for (int j = 0; j < contour.size(); j++) {
					/*
					int c1 = bin.at<uchar>(boundRect[i].x+1, boundRect[i].y+1);
					int c2 = bin.at<uchar>(boundRect[j].x+1, boundRect[j].y+1);
					*/
					if ((boundRect[i].y - boundRect[j].y) < 10 and (boundRect[i].y - boundRect[j].y) > -10 and i != j and boundRect[i].height > 20 and /*c1 == c2*/ ) {
						rectangle(frame, boundRect[i].tl(), boundRect[j].br(), Scalar(255, 0, 0), 2);//框出图形
						Point points((boundRect[i].x + boundRect[j].x + boundRect[j].width) / 2, (boundRect[i].y + (boundRect[j].height) / 2));
						//cout << (boundRect[i].x + boundRect[j].x + boundRect[j].width) / 2 << endl;
						circle(frame, points, 5, Scalar(0, 0, 255), -1);
					}
				}
			}
		}
		imshow(" test", frame);
		waitKey(1);
	}
	input.release();
	return 0;
}
