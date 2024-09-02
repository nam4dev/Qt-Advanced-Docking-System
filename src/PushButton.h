#ifndef PushButtonH
#define PushButtonH
//============================================================================
/// \file   PushButton.h
/// \author Uwe Kindler
/// \date   18.10.2022
/// \brief  Declaration of CPushButton
//============================================================================

//============================================================================
//                                   INCLUDES
//============================================================================
#include "ads_globals.h"

#include <QPushButton>

namespace ads
{

/**
 * ADS specific push button class with orientation support
 */
class ADS_EXPORT CPushButton : public QPushButton
{
    Q_OBJECT
public:
    enum Orientation {
        Horizontal,
        VerticalTopToBottom,
        VerticalBottomToTop
    };

    using QPushButton::QPushButton;

    [[nodiscard]] QSize sizeHint() const override;

    /**
     * Returns the current orientation
     */
    [[nodiscard]] Orientation buttonOrientation() const;

    /**
     * Set the orientation of this button
     */
    void setButtonOrientation(Orientation orientation);

protected:
    void paintEvent(QPaintEvent *event) override;

private:
    Orientation m_Orientation = Horizontal;
};

} // namespace ads

//---------------------------------------------------------------------------
#endif // PushButtonH

