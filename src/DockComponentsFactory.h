#ifndef DockComponentsFactoryH
#define DockComponentsFactoryH
//============================================================================
/// \file   DockComponentsFactory.h
/// \author Uwe Kindler
/// \date   10.02.2020
/// \brief  Declaration of DockComponentsFactory
//============================================================================

//============================================================================
//                                   INCLUDES
//============================================================================
#include "ads_globals.h"

namespace ads
{
class CDockWidgetTab;
class CDockAreaTitleBar;
class CDockAreaTabBar;
class CDockAreaWidget;
class CDockWidget;
class CAutoHideTab;

/**
 * Factory for creation of certain GUI elements for the docking framework.
 */
class ADS_EXPORT CDockComponentsFactory
{
public:
    // Constructor
    CDockComponentsFactory() {}

    // Destructor
    virtual ~CDockComponentsFactory() {}

    virtual CDockWidgetTab* createDockWidgetTab(CDockWidget* DockWidget);
    virtual CAutoHideTab* createDockWidgetSideTab(CDockWidget* DockWidget);
    virtual CDockAreaTabBar* createDockAreaTabBar(CDockAreaWidget* DockArea);
    virtual CDockAreaTitleBar* createDockAreaTitleBar(CDockAreaWidget* DockArea);
};

} // namespace ads

#endif // DockComponentsFactoryH
